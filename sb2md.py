import json
import os
import sys

def read_json(json_file):
    with open(json_file, "r", encoding='utf-8') as fin:
        contents = json.load(fin)
    return contents


def main():
    json_file = sys.argv[1] #"test/shin-note_20220121_131106.json" 
    json_content = read_json(json_file)
    outdir = json_content['name']
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    print(json_content.keys())
    pages = json_content['pages']
    for i, page in enumerate(pages):
        print(f"\nPage No. {i}")
        print(page['title'])
        title = page['title'].replace('/','-') 
        # ^ This replacement is to avoid the error of openinig file below.
        # If title includes /, open() may say "Not such a directory".

        with open(f"{outdir}/{title}.md", 'w') as fout:
            fout.write(f"# {page['title']}\n")
            fout.write(f"Created: {page['created']}\n") 
            fout.write(f"Updated: {page['created']}\n")
             
            iscode = False
            for line in page["lines"][1:]:
                print(line)

                if line.startswith("[**"):
                    line = line.replace('[**','').replace(']','')
                    fout.write(f"## {line}\n")

                elif not line.startswith(' ') and iscode: 
                    # Fri  6 May 2022 21:58:23 JST
                    # In a code block, there is a single space at the top. 
                    # So, the space is used to judge if a line is in a code block.
                    fout.write(f"```\n{line}\n")
                    iscode = False

                # $ indicates a oneline command in scrapbox, so it is replaced with `$ `.
                elif line.startswith("$"):
                    line = line.replace('$ ','`$ ') + '`'
                    fout.write(f"{line}\n")

                elif line.startswith("code"):
                    line = line.replace('code:','```')
                    fout.write(f"{line}\n")
                    iscode = True

                else:
                    line = line.replace('[','[[').replace(']',']]')
                    fout.write(f"{line}\n")
                
        print(page["lines"])

if __name__ == "__main__":
    main()
