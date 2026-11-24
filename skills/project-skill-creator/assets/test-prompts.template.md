# Test prompts for `<skill-name>`

Run each prompt in a fresh session and note whether the skill activated and the result was correct.

| # | Prompt | Expected |
|---|--------|----------|
| 1 | A direct request that clearly matches the description | Skill activates; follows the steps; meets the "done" criteria |
| 2 | The same need phrased differently (no skill keywords) | Skill still activates |
| 3 | A nearby request that is out of scope | Skill does NOT activate; agent answers normally |

If prompt 1 or 2 fails to activate, improve the description (add the words the user really used). If prompt 3 activates, add an explicit "Do not use for ..." sentence.
