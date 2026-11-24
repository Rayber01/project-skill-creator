---
name: laravel-migration
description: Creates Laravel database migrations that follow the project naming and safety conventions (reversible down method, indexes, foreign keys). Use when the user asks to add, change or drop a table or column in a Laravel project. Do not use for seeding data or editing Eloquent models only.
---

# Laravel migration

Generate a safe, reversible migration that matches the project conventions.

## Steps
1. Read `references/conventions.md` for naming, column types and index rules.
2. Check existing migrations in `database/migrations/` for the table's current shape so the new migration does not conflict.
3. Run `php artisan make:migration <descriptive_snake_case_name>` (add `--create=<table>` or `--table=<table>` as appropriate).
4. Implement `up()` and a real `down()` that exactly reverses it.
5. Add indexes and foreign keys as described in the conventions.
6. Run `php artisan migrate --pretend` and review the SQL. Do not run the real migration unless the user asks.

## Done when
- The migration file exists, `down()` reverses `up()`, and the pretend run shows the expected SQL.
