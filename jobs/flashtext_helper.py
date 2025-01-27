from flashtext import KeywordProcessor

def extract_skills(text, skill_list):
    processor = KeywordProcessor()
    processor.add_keywords_from_list(skill_list)
    return list(set(processor.extract_keywords(text)))
