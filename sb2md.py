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
#    print(pages)
    for i, page in enumerate(pages):
        print(f"\nPage No. {i}")
        print(page['title'])
        title = page['title'].replace('/','-') 
        # ^ This replacement is to avoid the error of openinig file below.
        # If title includes /, open() may say "Not such a directory".

        with open(f"{outdir}/{title}.md", 'w') as fout:
            fout.write(f"# {page['title']}\n")
            fout.write(f"Created: [[{page['created']}]]\n") 
            fout.write(f"Updated: [[{page['updated']}]]\n")
             
            iscode = False
            for line in page["lines"][1:]:
                print(line)

                if line.startswith("[**"):
                    line = line.replace('[**','').replace(']','')
                    fout.write(f"## {line}\n")

                # [$ ] indicates an equation, and is replaced with $ $.
                # Note: if several equations are in a line, this if-statement does not work properly. 
                # This is currenly only for one equation in a line.
                elif "[$" in line:
                    line = line.replace('[$ ','$')
                    idx_lastbrace = line.rfind(']')# Find the last match ']'
                    line_list     = list(line)
                    line_list[idx_lastbrace] = '$' # last "]" is replaced with $
                    line = "".join(line_list)      # converting to a string
                    fout.write(f"{line}\n")

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

                # In scrapbox, [ ] denotes a link, which is converted to '[[ ]]' for obsidian link format.
                elif '[$' not in line:
                    # ^ meaning there does not exist an equation in a line.
                    # Why do so? Because I dont' want to replace non-link braces with [[ ]].
                    line = line.replace('[','[[').replace(']',']]')
                    fout.write(f"{line}\n")
                
        #print(page["lines"])

if __name__ == "__main__":
    main()
