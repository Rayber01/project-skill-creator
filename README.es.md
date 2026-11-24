# Project Skill Creator

[English](README.md) | **Español**

Una [Agent Skill](https://agentskills.io/specification) abierta y neutral respecto al agente, que permite a los agentes de IA diseñar, validar e instalar **sus propias skills a medida del proyecto**. Apunta tu agente a un repositorio y pídele una skill: leerá el proyecto, decidirá qué merece ser skill, redactará un `SKILL.md` correcto, lo validará, te dará prompts de prueba y lo instalará en el lugar adecuado.

Funciona con opencode, Claude Code, Gemini CLI, Google Antigravity y Codex. Para ChatGPT, Gemini y Claude en la web hay prompts de chat listos para pegar.

## Por qué

- Las skills son más útiles cuando recogen las convenciones de **tu** proyecto, pero escribir buenas skills es delicado: una `description` débil hace que nunca se active, y cada agente busca en una carpeta distinta.
- Esta skill da a cualquier agente un flujo repetible, un árbol de decisión (skill vs regla en `AGENTS.md` vs script vs comando vs subagente), una checklist de calidad y un validador.

## Inicio rápido

```bash
git clone https://github.com/Rayber01/project-skill-creator.git
cd project-skill-creator

# Instalar en el proyecto actual para agentes que leen .agents/skills (opencode, Codex, Gemini CLI, Antigravity)
bash adapters/install.sh --agent agents --project-dir /ruta/a/tu/proyecto

# O elige tu agente / ámbito global
bash adapters/install.sh --agent opencode --scope global
bash adapters/install.sh --agent claude --project-dir /ruta/a/tu/proyecto
bash adapters/install.sh --list            # muestra todas las rutas destino
```
Después, en tu agente: *"Usa la skill project-skill-creator para analizar este repo y proponer skills para nuestros flujos recurrentes."*

### Otras formas de instalar
| Dónde | Cómo |
|---|---|
| Cualquier agente, a mano | Copia `skills/project-skill-creator/` a la carpeta de skills del agente (ver tabla) |
| Gemini CLI | `gemini skills install https://github.com/Rayber01/project-skill-creator.git` (o `gemini skills link <dir>`) |
| Claude.ai / Claude Desktop | `bash adapters/package.sh` y sube `dist/project-skill-creator.zip` en los ajustes de Skills |
| ChatGPT, Gemini web, otros | Pega [`adapters/chat-prompt.es.md`](adapters/chat-prompt.es.md) como instrucciones personalizadas, un Gem o prompt de proyecto |

### Dónde lee skills cada agente
| Agente | Proyecto | Global |
|---|---|---|
| opencode | `.opencode/skills/` (también `.claude/skills/`, `.agents/skills/`) | `~/.config/opencode/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Gemini CLI | `.gemini/skills/` o `.agents/skills/` | `~/.gemini/skills/` o `~/.agents/skills/` |
| Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |

Las rutas cambian entre versiones. La tabla completa, la matriz de cobertura y los enlaces oficiales (última verificación 2026-11-24) están en [`references/install-paths.md`](skills/project-skill-creator/references/install-paths.md). Instala cada skill en **una** sola ubicación por agente para evitar duplicados.

## Qué hace la skill

1. **Lee el proyecto**: stack, documentación, scripts, CI, skills existentes.
2. **Filtra candidatos** con un árbol de decisión con puntuación y dice dónde encaja cada uno (skill, `AGENTS.md`, script, comando, subagente, nada).
3. **Te entrevista** brevemente (máximo 3 preguntas) si faltan datos esenciales.
4. **Redacta** el `SKILL.md` desde una plantilla, con una descripción de una línea orientada a disparadores y divulgación progresiva.
5. **Valida** con `scripts/validate_skill.py`, o con una checklist manual si no hay consola.
6. **Da prompts de prueba**: dos que deben activarla y uno que no.
7. **Instala** tras preguntar agente y ámbito, sin sobrescribir sin permiso.
8. **Modo auditoría**: revisa y mejora las skills que ya tienes.

## Ejemplos de prompts
- "Analiza este repo y sugiere qué flujos nuestros deberían ser skills."
- "Crea una skill para cómo escribimos migraciones de base de datos aquí."
- "Audita las skills de `.agents/skills` y dime cuáles fusionar o eliminar."
- "Create a skill for our release process."

## Validador

```bash
python3 skills/project-skill-creator/scripts/validate_skill.py ruta/a/la/skill
python3 skills/project-skill-creator/scripts/validate_skill.py --all --strict skills examples
```
Comprueba: nombre y mayúsculas de `SKILL.md`, frontmatter, reglas de `name` y coincidencia con la carpeta, `description` en una sola línea (algunos agentes rechazan varias líneas), límites de longitud, enlaces internos, restos de TODO, nombres duplicados y posibles secretos. Solo biblioteca estándar.

## Estructura del repositorio

```
skills/project-skill-creator/   la skill: SKILL.md, references/, assets/, scripts/
adapters/                       install.sh, package.sh, prompts de chat (en/es)
examples/                       tres skills validadas + candidatos rechazados
tests/                          tests unitarios
.github/                        CI, workflow de release, plantillas de issues/PR
```

## Contribuir

Se agradecen issues y PRs, sobre todo **actualizaciones de rutas por agente**, **ejemplos** y **traducciones**. Mira [CONTRIBUTING.md](CONTRIBUTING.md). Las skills pueden ejecutar código: lee [SECURITY.md](SECURITY.md) y revisa cualquier skill antes de instalarla.

## Licencia

[MIT](LICENSE)
