# Agenti pro projekt „Django – Školní knihovna“

Tato složka obsahuje specializované agenty pro OpenCode.
Agenti jsou navrženi tak, aby tě provedli od základů Django až po nasazení a dokumentaci.

## Doporučené pořadí

1. `@01-roadmap-coach` – vytvoř roadmapu, milestone a GitHub verzování.
2. `@02-django-foundation` – založ projekt, app strukturu a stabilní konfiguraci.
3. `@04-library-domain` – implementuj modely knih, autorů, kategorií, příloh.
4. `@03-auth-oauth` – přidej lokální auth + OAuth (Google, Microsoft, GitHub).
5. `@05-circulation-and-reviews` – rezervace, výpůjčky, hodnocení a recenze.
6. `@06-ui-templates-ajax` – views, šablony, formuláře, AJAX interakce.
7. `@07-admin-i18n-static` – admin customizace, i18n, static/media.
8. `@08-release-docs-presenter` – Docker deploy, RTD, prezentace, release flow.

## Jak agenty volat

- V konverzaci napiš např.:
  - `@01-roadmap-coach Navrhni detailní plán na 10 sprintů pro tento projekt.`
  - `@03-auth-oauth Připrav krok po kroku implementaci OAuth přes Google.`
  - `@08-release-docs-presenter Vytvoř první verzi Docker setupu a RTD osnovy.`

## Doporučený způsob práce

- Postupuj po malých krocích.
- Po každé fázi udělej commit + tag (např. `v0.1-setup`, `v0.2-models`, ...).
- Udržuj průběžně dokumentaci: co bylo cílem, co je hotové, co je další krok.
- Když je něco nejasné, vrať se na `@01-roadmap-coach` a uprav plán.
