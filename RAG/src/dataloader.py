import os

def load_data(folder_path):
    documents = []
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"文件夹不存在：{folder_path}")
    all_files = os.listdir(folder_path)
    for file in all_files:
        if file.endswith('.txt'):
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                name = os.path.splitext(file)[0]
            documents.append(
                {
                    'name': name,
                    'content': content 
                }
            )
    return documents

if __name__ == "__main__":
    path = "../data/genshin_impact_characters"
    data = load_data(path)
    print(f"成功加载 {len(data)} 个文档")
    if data:
        print(f"第一个文档：{data[0]['name']}")
        print(f"内容长度：{len(data[0]['content'])} 字符")
