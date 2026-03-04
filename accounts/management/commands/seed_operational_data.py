from datetime import timedelta
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.constants import LIBRARIAN_GROUP, READER_GROUP
from catalog.models import Author, Book, Category
from circulation.models import Loan, Reservation
from reviews.models import Rating, Review

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users and operational data for realistic local testing."

    def add_arguments(self, parser):
        parser.add_argument("--librarians", type=int, default=3)
        parser.add_argument("--readers", type=int, default=15)
        parser.add_argument("--min-books", type=int, default=30)
        parser.add_argument("--active-loans", type=int, default=25)
        parser.add_argument("--returned-loans", type=int, default=35)
        parser.add_argument("--pending-reservations", type=int, default=20)
        parser.add_argument("--ratings", type=int, default=100)
        parser.add_argument("--reviews", type=int, default=70)
        parser.add_argument("--password", type=str, default="TestPass123!")
        parser.add_argument("--seed", type=int, default=20260304)

    @transaction.atomic
    def handle(self, *args, **options):
        rng = random.Random(options["seed"])

        librarian_group, _ = Group.objects.get_or_create(name=LIBRARIAN_GROUP)
        reader_group, _ = Group.objects.get_or_create(name=READER_GROUP)

        librarians = self._ensure_librarians(options["librarians"], options["password"], librarian_group)
        readers = self._ensure_readers(options["readers"], options["password"], reader_group)
        books = self._ensure_books(options["min_books"], rng)

        ratings_total = self._seed_ratings(readers, books, options["ratings"], rng)
        reviews_total = self._seed_reviews(readers, librarians, books, options["reviews"], rng)
        returned_total = self._seed_returned_loans(readers, librarians, books, options["returned_loans"], rng)
        active_total = self._seed_active_loans(readers, librarians, books, options["active_loans"], rng)
        pending_total = self._seed_pending_reservations(readers, books, options["pending_reservations"], rng)

        self.stdout.write(self.style.SUCCESS("Seed provozních dat dokončen."))
        self.stdout.write(f"Knihovníci: {len(librarians)}")
        self.stdout.write(f"Čtenáři: {len(readers)}")
        self.stdout.write(f"Knihy: {len(books)}")
        self.stdout.write(f"Hodnocení: {ratings_total}")
        self.stdout.write(f"Recenze: {reviews_total}")
        self.stdout.write(f"Výpůjčky (aktivní): {active_total}")
        self.stdout.write(f"Výpůjčky (vrácené): {returned_total}")
        self.stdout.write(f"Rezervace (čekající): {pending_total}")
        self.stdout.write(f"Heslo pro nové účty: {options['password']}")

    def _ensure_librarians(self, count, password, group):
        result = []
        for index in range(1, count + 1):
            username = f"librarian{index:02d}"
            user = self._create_or_update_user(
                username=username,
                email=f"{username}@library.local",
                first_name=f"Knihovník{index}",
                last_name="Testovací",
                password=password,
                is_staff=True,
                is_superuser=False,
            )
            user.groups.add(group)
            result.append(user)
        return result

    def _ensure_readers(self, count, password, group):
        result = []
        for index in range(1, count + 1):
            username = f"reader{index:02d}"
            user = self._create_or_update_user(
                username=username,
                email=f"{username}@library.local",
                first_name=f"Čtenář{index}",
                last_name="Testovací",
                password=password,
                is_staff=False,
                is_superuser=False,
            )
            user.groups.add(group)
            result.append(user)
        return result

    def _create_or_update_user(self, *, username, email, first_name, last_name, password, is_staff, is_superuser):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": is_staff,
                "is_superuser": is_superuser,
            },
        )
        if created:
            user.set_password(password)
            user.save()
        else:
            updated = False
            if user.email != email:
                user.email = email
                updated = True
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if user.last_name != last_name:
                user.last_name = last_name
                updated = True
            if user.is_staff != is_staff:
                user.is_staff = is_staff
                updated = True
            if user.is_superuser != is_superuser:
                user.is_superuser = is_superuser
                updated = True
            if updated:
                user.save(update_fields=["email", "first_name", "last_name", "is_staff", "is_superuser"])
        return user

    def _ensure_books(self, min_books, rng):
        books = list(Book.objects.all())
        if len(books) >= min_books:
            return books

        category_names = ["Román", "Detektivka", "Sci-fi", "Historie", "Naučná", "Drama"]
        categories = [Category.objects.get_or_create(name=name, defaults={"description": f"Kategorie {name}"})[0] for name in category_names]

        first_names = ["Jan", "Anna", "Petr", "Eva", "Tomáš", "Lucie", "Marek", "Jana"]
        last_names = ["Novák", "Svoboda", "Dvořák", "Černá", "Procházka", "Beneš", "Marek", "Veselý"]
        authors = []
        for index in range(1, 13):
            author, _ = Author.objects.get_or_create(
                first_name=first_names[(index - 1) % len(first_names)],
                last_name=f"{last_names[(index - 1) % len(last_names)]}{index}",
                defaults={"biography": f"Biografie autora {index}."},
            )
            authors.append(author)

        next_index = len(books) + 1
        while len(books) < min_books:
            isbn = str(9788099000000 + next_index)
            book, _ = Book.objects.get_or_create(
                isbn=isbn,
                defaults={
                    "title": f"Testovací kniha {next_index}",
                    "subtitle": "Demo data pro provozní testování",
                    "publication_year": 2000 + (next_index % 25),
                    "language": rng.choice([choice[0] for choice in Book.Language.choices]),
                    "description": f"Automaticky generovaná testovací kniha {next_index}.",
                    "copies_total": rng.randint(1, 3),
                    "is_available": True,
                },
            )
            chosen_authors = rng.sample(authors, k=rng.randint(1, 2))
            book.authors.set(chosen_authors)
            book.categories.set(rng.sample(categories, k=rng.randint(1, 2)))
            books.append(book)
            next_index += 1
        return books

    def _seed_ratings(self, readers, books, target_count, rng):
        pairs = [(reader, book) for reader in readers for book in books]
        rng.shuffle(pairs)
        total = 0
        for reader, book in pairs[:target_count]:
            score = rng.randint(1, 5)
            Rating.objects.update_or_create(user=reader, book=book, defaults={"score": score})
            total += 1
        return total

    def _seed_reviews(self, readers, librarians, books, target_count, rng):
        statuses = [Review.Status.PENDING, Review.Status.APPROVED, Review.Status.REJECTED]
        pairs = [(reader, book) for reader in readers for book in books]
        rng.shuffle(pairs)
        total = 0
        now = timezone.now()

        for index, (reader, book) in enumerate(pairs[:target_count], start=1):
            status = rng.choices(statuses, weights=[2, 5, 2], k=1)[0]
            defaults = {
                "text": f"Testovací recenze č. {index} pro knihu '{book.title}'.",
                "status": status,
                "moderation_note": "",
                "moderated_by": None,
                "moderated_at": None,
            }
            if status in {Review.Status.APPROVED, Review.Status.REJECTED}:
                defaults["moderated_by"] = rng.choice(librarians)
                defaults["moderated_at"] = now - timedelta(days=rng.randint(0, 45))
                if status == Review.Status.REJECTED:
                    defaults["moderation_note"] = "Nevhodný nebo málo přínosný obsah."

            Review.objects.update_or_create(user=reader, book=book, defaults=defaults)
            total += 1
        return total

    def _seed_returned_loans(self, readers, librarians, books, target_count, rng):
        pairs = [(reader, book) for reader in readers for book in books]
        rng.shuffle(pairs)
        total = 0
        now = timezone.now()

        for reader, book in pairs:
            if total >= target_count:
                break
            borrowed_at = now - timedelta(days=rng.randint(20, 120))
            due_date = (borrowed_at + timedelta(days=14)).date()
            returned_at = borrowed_at + timedelta(days=rng.randint(2, 25))
            if returned_at > now:
                returned_at = now - timedelta(days=1)

            loan, created = Loan.objects.get_or_create(
                borrower=reader,
                book=book,
                status=Loan.Status.RETURNED,
                defaults={
                    "handled_by": rng.choice(librarians),
                    "due_date": due_date,
                    "returned_at": returned_at,
                },
            )
            if not created:
                loan.handled_by = rng.choice(librarians)
                loan.due_date = due_date
                loan.returned_at = returned_at
                loan.save()
            total += 1
        return total

    def _seed_active_loans(self, readers, librarians, books, target_count, rng):
        total = 0
        now = timezone.now()
        book_pool = books[:]
        rng.shuffle(book_pool)

        for book in book_pool:
            if total >= target_count:
                break

            active_for_book = Loan.objects.filter(book=book, status=Loan.Status.ACTIVE).count()
            available_slots = max(0, book.copies_total - active_for_book)
            if available_slots == 0:
                continue

            candidates = readers[:]
            rng.shuffle(candidates)
            for reader in candidates:
                if total >= target_count or available_slots <= 0:
                    break
                exists = Loan.objects.filter(book=book, borrower=reader, status=Loan.Status.ACTIVE).exists()
                if exists:
                    continue

                is_overdue = rng.random() < 0.25
                due_date = (now - timedelta(days=rng.randint(1, 10))).date() if is_overdue else (now + timedelta(days=rng.randint(2, 20))).date()
                borrowed_days_ago = rng.randint(1, 30)
                borrowed_at = now - timedelta(days=borrowed_days_ago)

                loan = Loan(
                    borrower=reader,
                    book=book,
                    handled_by=rng.choice(librarians),
                    status=Loan.Status.ACTIVE,
                    due_date=due_date,
                )
                loan.save()
                Loan.objects.filter(pk=loan.pk).update(borrowed_at=borrowed_at)

                total += 1
                available_slots -= 1

        return total

    def _seed_pending_reservations(self, readers, books, target_count, rng):
        total = 0
        now = timezone.now()
        books_ranked = sorted(
            books,
            key=lambda item: Loan.objects.filter(book=item, status=Loan.Status.ACTIVE).count() - item.copies_total,
            reverse=True,
        )

        for book in books_ranked:
            if total >= target_count:
                break

            active_count = Loan.objects.filter(book=book, status=Loan.Status.ACTIVE).count()
            if active_count < book.copies_total:
                continue

            reader_pool = readers[:]
            rng.shuffle(reader_pool)
            for reader in reader_pool:
                if total >= target_count:
                    break

                if Loan.objects.filter(book=book, borrower=reader, status=Loan.Status.ACTIVE).exists():
                    continue

                reservation, created = Reservation.objects.get_or_create(
                    book=book,
                    requester=reader,
                    status=Reservation.Status.PENDING,
                )
                if created:
                    expires_at = now + timedelta(days=rng.randint(1, 10))
                    Reservation.objects.filter(pk=reservation.pk).update(reserved_at=now - timedelta(days=rng.randint(0, 5)), expires_at=expires_at)
                    total += 1

        return total
