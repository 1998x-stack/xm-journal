"""Build the lightweight offline-first xm-journal site."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"_site"
def main():
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir()
    for rel in ("journal","reports","data"):
        src=ROOT/rel
        if src.exists(): shutil.copytree(src,OUT/rel,dirs_exist_ok=True)
    shutil.copy2(ROOT/"site/index.html",OUT/"index.html")
    shutil.copytree(ROOT/"site/assets",OUT/"assets",dirs_exist_ok=True)
    print(f"Built {OUT}")
if __name__=="__main__": main()
