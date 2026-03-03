import re

def split_by_sections(text: str, character_name: str) -> list:
    """
    按章节标题分片
    """
    chunks = []
    current_chunk = []
    current_section = "角色简介"
    
    pattern = r'(?=\s*[一二三四五六七八九十百千万零]+、)'

    lines = text.splitlines()

    for line in lines:
        if re.match(pattern,line):
            if current_chunk:
                content = ''.join(current_chunk).strip()
                if content:
                    content = f"""【角色】{character_name}
【章节】{current_section}
【内容】{content}""".strip()
                    chunks.append({
                        'content': content,
                        'metadata': {
                            'character': character_name,
                            'section': current_section
                        }
                    })
            current_chunk = [line]
            current_section = re.sub(pattern, '', line).strip()
        else:
            current_chunk.append(line)
    if current_chunk:
        content = '\n'.join(current_chunk).strip()
        if content:
            content = f"""【角色】{character_name}
【章节】{current_section}
【内容】{content}""".strip()
            chunks.append({
                'content': content,
                'metadata': {
                    'character': character_name,
                    'section': current_section
                }
            })
    return chunks

if __name__ == '__main__':
    path = "../data/genshin_impact_characters/Columbina_Hyposelenia.txt"
    name = "Columbina_Hyposelenia"
    with open(path,'r',encoding='utf-8') as f:
        chunk = split_by_sections(f.read(),name)
    print(chunk)