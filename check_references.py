#!/usr/bin/env python3
"""
参考文献链接检测脚本
检测LaTeX文档中所有参考文献链接的可用性和准确性
"""

import re
import requests
from urllib.parse import urlparse
import time
from typing import List, Tuple, Dict

# 从LaTeX文件中提取的所有URL
URLS = [
    # ACL Anthology
    ("SemStamp NAACL 2024", "https://aclanthology.org/2024.naacl-long.226/"),
    ("SemaMark NAACL 2024", "https://aclanthology.org/2024.findings-naacl.40.pdf"),
    ("PostMark EMNLP 2024", "https://aclanthology.org/2024.emnlp-main.506/"),
    ("Duwak ACL 2024", "https://aclanthology.org/2024.findings-acl.678/"),
    ("GumbelSoft ACL 2024", "https://aclanthology.org/2024.acl-long.315/"),
    ("MorphMark ACL 2025", "https://aclanthology.org/2025.acl-long.240.pdf"),
    ("WaterBench ACL 2024", "https://aclanthology.org/2024.acl-long.83/"),
    ("WaterPark EMNLP 2025", "https://aclanthology.org/2025.findings-emnlp.1148/"),
    ("MCMARK ACL 2025", "https://aclanthology.org/2025.acl-long.391.pdf"),
    ("STA-1 ACL 2025", "https://aclanthology.org/2025.acl-long.1005.pdf"),
    ("SCTS ACL 2024", "https://aclanthology.org/2024.acl-long.464/"),
    ("WaterJudge NAACL 2024", "https://aclanthology.org/2024.findings-naacl.223.xml"),
    ("ACL Tutorial 2024", "https://aclanthology.org/2024.acl-tutorials.6/"),
    
    # ICML/MLR Press
    ("Adaptive Text Watermark ICML 2024", "https://proceedings.mlr.press/v235/liu24e.html"),
    ("KGW ICML 2023", "https://proceedings.mlr.press/v202/kirchenbauer23a/kirchenbauer23a.pdf"),
    
    # ICLR
    ("Reliability ICLR 2024", "https://proceedings.iclr.cc/paper_files/paper/2024/hash/d78e9e4316e1714fbb0f20be66f8044c-Abstract-Conference.html"),
    ("Unbiased ICLR 2024", "https://proceedings.iclr.cc/paper_files/paper/2024/hash/c5b00c5bdcc6fe35907dbcca03d27652-Abstract-Conference.html"),
    ("UPV ICLR 2024", "https://proceedings.iclr.cc/paper_files/paper/2024/hash/214d2cffc381938be6f7254d5382904f-Abstract-Conference.html"),
    
    # NeurIPS
    ("No Free Lunch NeurIPS 2024", "https://proceedings.neurips.cc/paper_files/paper/2024/file/fa86a9c7b9f341716ccb679d1aeb9afa-Paper-Conference.pdf"),
    
    # ArXiv
    ("Watermarks in the Sand", "https://arxiv.org/abs/2306.04634"),
    ("Watermark Stealing", "https://arxiv.org/abs/2310.07710v1"),
    ("Exploiting Strengths", "https://arxiv.org/abs/2402.19361"),
    ("Multi-bit Watermark", "https://arxiv.org/abs/2402.16187"),
    
    # Other
    ("Nature SynthID-Text", "https://www.nature.com/articles/s41586-024-08025-4.pdf"),
    ("GitHub MarkLLM", "https://github.com/THU-BPM/MarkLLM"),
    ("OpenReview DiPmark", "https://openreview.net/forum?id=rIOl7KbSkv"),
    ("Cross-lingual Watermark", "https://cross-lingual-watermark.github.io/"),
    ("StealthInk GMU", "https://napl.gmu.edu/pubs/CPapers/Jiang-StealthInk-ICML2025.pdf"),
    ("IACR Multi-User", "https://eprint.iacr.org/2024/759.pdf"),
    ("USENIX Security REMARK", "https://www.usenix.org/conference/usenixsecurity24/presentation/zhang-ruisi"),
    ("ACM Computing Surveys", "https://dlnext.acm.org/doi/pdf/10.1145/3691626"),
    ("ACL Tutorial Leililab", "https://leililab.github.io/llm_watermark_tutorial/ACL-tut-LLM-watermark-part-5.pdf"),
]

def check_url(name: str, url: str, timeout: int = 10) -> Tuple[bool, str, int]:
    """
    检查URL的可用性
    返回: (是否可用, 状态信息, HTTP状态码)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.head(url, allow_redirects=True, timeout=timeout, headers=headers)
        status_code = response.status_code
        
        if status_code == 200:
            return True, "[OK] Available", status_code
        elif status_code in [301, 302, 303, 307, 308]:
            final_url = response.url
            if final_url != url:
                return True, f"[OK] Redirected to: {final_url}", status_code
            return True, "[OK] Available (redirect)", status_code
        elif status_code == 403:
            # 尝试GET请求
            try:
                get_response = requests.get(url, timeout=timeout, headers=headers)
                if get_response.status_code == 200:
                    return True, "[OK] Available (needs GET)", get_response.status_code
            except:
                pass
            return False, "[FAIL] Forbidden (403)", status_code
        elif status_code == 404:
            return False, "[FAIL] Not Found (404)", status_code
        else:
            return False, f"[FAIL] HTTP Error ({status_code})", status_code
            
    except requests.exceptions.Timeout:
        return False, "[FAIL] Timeout", 0
    except requests.exceptions.ConnectionError:
        return False, "[FAIL] Connection Error", 0
    except requests.exceptions.TooManyRedirects:
        return False, "[FAIL] Too Many Redirects", 0
    except requests.exceptions.RequestException as e:
        return False, f"[FAIL] Request Error: {str(e)[:50]}", 0
    except Exception as e:
        return False, f"[FAIL] Unknown Error: {str(e)[:50]}", 0

def main():
    print("=" * 80)
    print("Reference Link Check Report")
    print("=" * 80)
    print()
    
    results = []
    available_count = 0
    unavailable_count = 0
    
    for name, url in URLS:
        print(f"Checking: {name}")
        print(f"  URL: {url}")
        
        is_available, message, status_code = check_url(name, url)
        results.append((name, url, is_available, message, status_code))
        
        if is_available:
            available_count += 1
            print(f"  Status: {message}")
        else:
            unavailable_count += 1
            print(f"  Status: {message}")
        
        print()
        time.sleep(0.5)  # Avoid too frequent requests
    
    # 生成报告
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total: {len(URLS)} links")
    print(f"Available: {available_count} links")
    print(f"Unavailable: {unavailable_count} links")
    print()
    
    if unavailable_count > 0:
        print("Unavailable Links:")
        print("-" * 80)
        for name, url, is_available, message, status_code in results:
            if not is_available:
                print(f"  [FAIL] {name}")
                print(f"    {url}")
                print(f"    Status: {message}")
                print()
    
    print("Available Links:")
    print("-" * 80)
    for name, url, is_available, message, status_code in results:
        if is_available:
            print(f"  [OK] {name}")
            if "Redirect" in message:
                print(f"    {message}")
            print()
    
    # 保存报告到文件
    with open("reference_check_report.txt", "w", encoding="utf-8") as f:
        f.write("Reference Link Check Report\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Check Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {len(URLS)} links\n")
        f.write(f"Available: {available_count} links\n")
        f.write(f"Unavailable: {unavailable_count} links\n\n")
        
        if unavailable_count > 0:
            f.write("Unavailable Links:\n")
            f.write("-" * 80 + "\n")
            for name, url, is_available, message, status_code in results:
                if not is_available:
                    f.write(f"[FAIL] {name}\n")
                    f.write(f"  {url}\n")
                    f.write(f"  Status: {message}\n\n")
        
        f.write("All Links Details:\n")
        f.write("-" * 80 + "\n")
        for name, url, is_available, message, status_code in results:
            status_symbol = "[OK]" if is_available else "[FAIL]"
            f.write(f"{status_symbol} {name}\n")
            f.write(f"  {url}\n")
            f.write(f"  Status: {message}\n\n")
    
    print(f"\nDetailed report saved to: reference_check_report.txt")

if __name__ == "__main__":
    main()

