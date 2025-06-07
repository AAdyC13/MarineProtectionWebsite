# python manage.py test CORE.corpus_load
import pdfplumber
import os
import chardet
import trafilatura
from .models import cleanText as ct
from .utils import add_loaded_corpus
from .utils import get_loaded_corpus
from .utils import del_loaded_corpus

base_path = "C:\\Users\\AAdy\\Desktop\\開發環境\\海洋保護宣傳網站\\語料庫"


def corpus_load_in():
    print(f"ℹ️ 開始載入語料庫")
    loaded_corpus: list = get_loaded_corpus().keys()
    new_corpus: list = [i for i in os.listdir(
        base_path) if i not in loaded_corpus]

    print(f"ℹ️ 本次共新增 {len(new_corpus)} 個語料庫：")
    for name in new_corpus:
        print(f"  - {name}")

    for corpus in new_corpus:
        print(f"ℹ️ 開始讀取 {corpus} 語料庫")
        inner_path = f"{base_path}\\{corpus}"

        with open(f"{inner_path}\\url_list_final.txt", 'r', encoding='utf-8', errors='ignore') as f:
            url_list_final = f.read().split("\n")

        with open(f"{inner_path}\\seeds.txt", 'r', encoding='utf-8', errors='ignore') as f:
            seed = [line.strip()
                    for line in f.read().split("\n") if line.strip()]

        file_list = os.listdir(f"{inner_path}\\download")
        counter = -1
        for filename in file_list:
            counter += 1
            # if counter >= 10:
            #     break
            # title
            title, ext = os.path.splitext(filename)
            if int(title.split("_")[3]) != counter:
                print(f"⚠️  文件 {counter} 不存在")
                counter += 1
            try:
                if filename.endswith('.html') or filename.endswith('.htm'):
                    file_path = f"{inner_path}\\download\\{filename}"
                    # 先以二進位讀取前部分內容來偵測編碼
                    with open(file_path, 'rb') as f:
                        raw_data = f.read(2048)
                        result = chardet.detect(raw_data)
                        # 預設 fallback utf-8
                        encoding = result['encoding'] or 'utf-8'
                    # 再用偵測到的編碼讀取整份檔案
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        html = f.read()

                    # 用 trafilatura 抽取正文
                    extracted_text = trafilatura.extract(html)
                    if extracted_text.strip():
                        data = {
                            "title": f"{title}",
                            "content": extracted_text.strip(),
                            "url": url_list_final[counter],
                        }
                        ct.db_update(data)
                        print(f'✅ 成功讀取：{filename}')

                elif filename.endswith('.pdf'):
                    # 處理 PDF 文件
                    try:
                        with pdfplumber.open(file_path) as pdf:
                            extracted_text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    extracted_text += page_text + "\n"
                        if extracted_text.strip():
                            data = {
                                "title": f"{title}",
                                "content": extracted_text.strip(),
                                "url": url_list_final[counter],
                            }
                            ct.db_update(data)
                            print(f'✅ 成功讀取：{filename}')
                        else:
                            print(f'🔴 無法擷取：{filename}')
                    except Exception as e:
                        print(f'🔴 PDF讀取錯誤：{filename} - {e}')
            except Exception as e:
                print(f'🔴 讀取錯誤：{filename}')
        else:
            print(f'🔴 非可寫入：{filename}')

        add_loaded_corpus(corpus, seed)
        print(f"ℹ️ 種子： {seed}")
        print(f"ℹ️ 語料庫 {corpus} 載入完畢")

    print(f"ℹ️ 語料庫載入完畢")


def extract_text_from_pdf_pdfplumber(file_path):
    """使用 pdfplumber 抽取 PDF 文字（更準確）"""
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()
    except Exception as e:
        print(f"讀取PDF錯誤: {e}")
        return None


def corpus_del(name):
    del_loaded_corpus(name)


# corpus_del("pl_jp_01")
corpus_load_in()
