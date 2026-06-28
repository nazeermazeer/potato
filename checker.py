import language_tool_python
from dataclasses import dataclass

tool = language_tool_python.LanguageTool('en-US')
tool.picky = True


@dataclass
class CustomMatch:
    rule_id: str
    message: str
    context: str
    replacements: list[str]
    offset: int
    error_length: int
    
# def correct_strictly(text, lang='en-US'):
#     # Initialize tool with picky mode set to True
#     tool = language_tool_python.LanguageTool(lang)
#     tool.picky = True  
    
#     max_passes = 5
#     current_pass = 0
    
#     while current_pass < max_passes:
#         # Get all matches, ignoring basic stylistic preferences if desired
#         matches = tool.check(text)
        
#         # Filter for strict grammar/spelling (skipping pure stylistic warnings if wanted)
#         strict_matches = [m for m in matches if m.ruleId not in ['UPPERCASE_SENTENCE_START', 'WHITESPACE_RULE']]
        
#         if not strict_matches:
#             break
            
#         # Apply corrections
#         new_text = tool.correct(text)
        
#         # Stop if no further changes are being made
#         if new_text == text:
#             break
            
#         text = new_text
#         current_pass += 1
        
#     tool.close()
#     return text


def check_sentence_punctuation(value: str) -> list[CustomMatch]:
    stripped = value.strip()
    if not stripped or stripped[-1] in ".!?":
        return []

    return [
        CustomMatch(
            rule_id="MISSING_SENTENCE_END_PUNCTUATION",
            message="This sentence does not end with punctuation.",
            context=value,
            replacements=[f"{stripped}."],
            offset = len(value),
            error_length = 1
        )
    ]


def enforce_sentence_punctuation(value: str) -> str:
    stripped = value.rstrip()
    if not stripped or stripped[-1] in ".!?":
        return value

    return f"{stripped}."

class Checker:
    def checkText(self, input):
        text = input
        matches = tool.check(text) + check_sentence_punctuation(text)
        return matches

    def getCorrectedText(self, text):
        correctedText = enforce_sentence_punctuation(tool.correct(text))
        return correctedText
