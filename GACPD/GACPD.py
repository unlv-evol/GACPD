import os
import sys
import json
import pandas as pd
import shutil
import subprocess
import matplotlib.pyplot as plt
import time
import Methods.totals as totals
import Methods.analysis as analysis
import Methods.analysis as analysis
import Methods.classifier as classifier
import Methods.dataLoader as dataloader
import Methods.common as common
import Methods.commitLoader as commitloader
from Methods.patchExtractionFunctions import divergence_date
from Methods.patchExtractionFunctions import pr_patches


class GACPD:
    def __init__(self, params):
        self.repo_check_number, self.repo_main_line, self.repo_divergent, self.token_list, self.divergence_date, self.cut_off_date = params
        self.token_count = len(self.token_list)
        self.repo_data = []
        self.results = {}
        self.main_dir_results = 'Results/Repos_results/'
        self.repo_dir_files = 'Results/Repos_files/'
        self.pr_classifications = {}
        self.prs = []
        self.file_extensions_swapped = {
            ".abap": "abap",
            ".as": "actionscript",
            ".ada": "ada",
            ".conf": "nginx",
            ".apl": "apl",
            ".applescript": "applescript",
            ".ino": "arduino",
            ".arff": "arff",
            ".adoc": "asciidoc",
            ".asm": "nasm",
            ".asp": "aspnet",
            ".ahk": "autohotkey",
            ".au3": "autoit",
            ".sh": "bash",
            ".bas": "basic",
            ".bat": "batch",
            ".y": "bison",
            ".bf": "brainfuck",
            ".bro": "bro",
            ".c": "c",
            ".clj": "clojure",
            ".coffee": "coffeescript",
            ".cpp": "cpp",
            ".cr": "crystal",
            ".cs": "csharp",
            ".csp": "csp",
            ".css": "css",
            ".d": "d",
            ".dart": "dart",
            ".diff": "diff",
            "Dockerfile": "docker",
            ".e": "eiffel",
            ".ex": "elixir",
            ".erb": "erb",
            ".erl": "erlang",
            ".f90": "fortran",
            ".fs": "fsharp",
            ".ged": "gedcom",
            ".feature": "gherkin",
            ".git": "git",
            ".glsl": "glsl",
            ".go": "go",
            ".graphql": "graphql",
            ".groovy": "groovy",
            ".haml": "haml",
            ".hbs": "handlebars",
            ".hs": "haskell",
            ".hx": "haxe",
            ".hpkp": "hpkp",
            ".hsts": "hsts",
            ".html": "html",
            ".http": "http",
            ".ijs": "j",
            ".icon": "icon",
            ".ni": "inform7",
            ".ini": "ini",
            ".io": "io",
            ".ipynb": "ipynb",
            ".java": "java",
            ".js": "javascript",
            ".ol": "jolie",
            ".json": "json",
            ".jsx": "jsx",
            ".jl": "julia",
            ".kmn": "keyman",
            ".kt": "kotlin",
            ".tex": "latex",
            ".less": "less",
            ".liquid": "liquid",
            ".lisp": "lisp",
            ".ls": "livescript",
            ".lol": "lolcode",
            ".lua": "lua",
            "Makefile": "makefile",
            ".md": "markdown",
            ".xml": "markup",
            ".m": "matlab",
            ".mel": "mel",
            ".miz": "mizar",
            ".monkey": "monkey",
            ".n4js": "n4js",
            ".nim": "nim",
            ".nix": "nix",
            ".nsi": "nsis",
            ".ml": "ocaml",
            ".cl": "opencl",
            ".oz": "oz",
            ".gp": "parigp",
            ".parser": "parser",
            ".pas": "pascal",
            ".pl": "prolog",
            ".php": "php",
            ".sql": "plsql",
            ".ps1": "powershell",
            ".pde": "processing",
            ".properties": "properties",
            ".proto": "protobuf",
            ".pug": "pug",
            ".pp": "puppet",
            ".pure": "pure",
            ".py": "python",
            ".q": "q",
            ".re": "reason",
            ".rpy": "renpy",
            ".rest": "rest",
            ".rip": "rip",
            ".graph": "roboconf",
            ".rb": "ruby",
            ".rs": "rust",
            ".sas": "sas",
            ".sass": "sass",
            ".scala": "scala",
            ".scm": "scheme",
            ".scss": "scss",
            ".st": "smalltalk",
            ".tpl": "smarty",
            ".soy": "soy",
            ".styl": "stylus",
            ".swift": "swift",
            ".tcl": "tcl",
            ".textile": "textile",
            ".tsx": "tsx",
            ".twig": "twig",
            ".ts": "typescript",
            ".vb": "visual_basic",
            ".vm": "velocity",
            ".v": "verilog",
            ".vhdl": "vhdl",
            ".vim": "vim",
            ".wasm": "wasm",
            ".wiki": "wiki",
            ".xeora": "xeora",
            ".xojo": "xojo",
            ".yaml": "yaml",
            ".yml": "yml",
        }
        self.pareco_extensions = ["c", "java", "python", "bash", "prolog", "php", "ruby"]

    def set_prs(self, prs):
        for pr in prs:
            self.prs.append(str(pr))

    def get_dates(self):
        self.fork_date, self.divergence_date, self.cut_off_date, self.ahead_by, self.behind_by, self.ct = divergence_date(
            self.repo_main_line, self.repo_divergent, self.token_list, self.token_count, self.cut_off_date, self.divergence_date)
        print(
            f'The divergence_date of the repository {self.repo_divergent} is {self.divergence_date} and the cut_off_date is {self.cut_off_date}.')
        print(f'The variant2 is ==>')
        print(f'\t Ahead by {self.ahead_by} patches')
        print(f'\t Behind by {self.behind_by} patches')
        print(
            f'Select an interval within the period [{self.divergence_date}, {self.cut_off_date}] to limit the patches being checked.')

    def createDf(self):
        df_data_files = []
        df_data_patches = []

        for pr in self.results:
            for file in self.results[pr]:
                try:
                    if self.results[pr][file]['result']['patchClass'] in ['ED', 'MO', 'SP']:
                        df_data_files.append(
                            [self.repo_main_line, self.repo_divergent, pr, file, self.results[pr][file]['result']['type'],
                             self.results[pr][file]['result']['patchClass'], 1])
                    else:
                        df_data_files.append([self.repo_main_line, self.repo_divergent, pr, file, 'None',
                                              self.results[pr][file]['result']['patchClass'], 0])
                    #print(self.results[pr][file])
                except Exception as e:
                    pass

            if self.pr_classifications[pr]["class"] in ['ED', 'MO', 'SP']:
                df_data_patches.append([self.repo_main_line, self.repo_divergent, pr, self.pr_classifications[pr]["class"], 1])
            else:
                df_data_patches.append([self.repo_main_line, self.repo_divergent, pr, self.pr_classifications[pr]["class"], 0])

        self.df_files_classes = pd.DataFrame(df_data_files,
                                             columns=['Mainline', 'Fork', 'Pr nr', 'Filename', 'Operation',
                                                      'File classification', 'Interesting'])
        self.df_files_classes = self.df_files_classes.sort_values(by=['Pr nr', 'Interesting'], ascending=False)

        self.df_patch_classes = pd.DataFrame(df_data_patches,
                                             columns=['Mainline', 'Fork', 'Pr nr', 'Patch classification',
                                                      'Interesting'])
        self.df_patch_classes = self.df_patch_classes.sort_values(by='Interesting', ascending=False)

    def printResults(self):
        print('\nClassification results:')
        for pr in self.results:
            print('\n')
            print(f'{self.repo_main_line} -> {self.repo_divergent}')
            print(f'Pull request nr ==> {pr}')
            #             print('\n')
            print('File classifications ==> ')
            for file in self.results[pr]:
                if self.results[pr][file]["result"]["patchClass"] in ['ED', 'MO', 'SP']:
                    print(f'\t {file}')
                    print(f'\t\t Operation - {self.results[pr][file]["result"]["type"]}')
                    print(f'\t\t Class - {self.results[pr][file]["result"]["patchClass"]}')
                else:
                    print(f'\t {file}')
                    print(f'\t\t Class - {self.results[pr][file]["result"]["patchClass"]}')
            print(f'Patch classification ==> {self.pr_classifications[pr]["class"]}')

    def parse_patch_file(self, patch_file, output_dir, extension):
        with open(patch_file, 'r') as patch:
            hunk_count = 0
            add_count = 0
            del_count = 0
            additions_file = []
            deletions_file = []

            for line in patch:
                # Detect the start of a new hunk (lines starting with "@@")
                if line.startswith('@@'):
                    if hunk_count >= 0:
                        self.save_hunk_files(hunk_count, output_dir, deletions_file, del_count, f"deletions.{extension}")
                        self.save_hunk_files(hunk_count, output_dir, additions_file, add_count, f"additions.{extension}")
                    hunk_count += 1
                    additions_file = []
                    deletions_file = []

                if line.startswith('+') and not line.startswith("+++"):
                    additions_file.append(line[1:])
                    add_count += 1
                elif line.startswith('-') and not line.startswith("---"):
                    deletions_file.append(line[1:])
                    del_count += 1
                elif not line.startswith("---") and not line.startswith("+++") and not line.startswith('@@'):
                    additions_file.append(line)
                    deletions_file.append(line)

            # Process the last hunk if any
            if deletions_file or additions_file:
                self.save_hunk_files(hunk_count, output_dir, deletions_file, del_count, f"deletions.{extension}")
                self.save_hunk_files(hunk_count, output_dir, additions_file, add_count, f"additions.{extension}")

    def save_hunk_files(self, hunk_id, output_dir, additions_hunks, counts, type_of_change):
        os.makedirs(output_dir, exist_ok=True)

        # Write the hunk with only additions to the additions file, if applicable
        if counts != 0:
            additions_file_path = os.path.join(output_dir, f'hunk_{hunk_id}_{type_of_change}')
            with open(additions_file_path, 'w') as add_file:
                add_file.writelines(additions_hunks)
            # print(f"Saved additions file for hunk {hunk_id}: {additions_file_path}")

    def extractPatches(self, chosen_diverge_date, chosen_cut_off_date):
        self.diverge_date = chosen_diverge_date
        self.cut_off_date = chosen_cut_off_date
        print(f'Extracting patches between {self.diverge_date} and {self.cut_off_date}...')

        pr_patch_ml_str = ''
        pr_title_ml_str = ''

        pr_patch_ml, pr_title_ml, pr_all_merged_ml, self.ct = pr_patches(self.repo_main_line, self.diverge_date,
                                                                         self.cut_off_date, self.token_list, self.ct)

        # at least one of the mainline or fork should have a pr with patch
        if len(pr_patch_ml) > 0:
            if len(pr_patch_ml) > 1:
                pr_patch_ml_str = '/'.join(map(str, pr_patch_ml))
                pr_title_ml_str = '=/='.join(map(str, pr_title_ml))
            if len(pr_patch_ml) == 1:
                pr_patch_ml_str = pr_patch_ml[0]
                pr_title_ml_str = pr_title_ml[0]

        df_data = []
        for i in range(len(pr_patch_ml)):
            df_data.append([pr_patch_ml[i], pr_title_ml[i]])

        self.df_patches = pd.DataFrame(df_data, columns=['Patch number', 'Patch title'])


        return pr_patch_ml

    def remove_all_files(self, directory_path):
        # Check if the directory exists
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            # Loop through all files and directories in the specified directory
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                try:
                    # Remove file if it's a file, or recursively delete if it's a directory
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
        else:
            print("The specified directory does not exist or is not a directory.")

    def visualizeResults(self):
        print(f'\nBar plot of the patch classifications for {self.repo_main_line} -> {self.repo_divergent}')
        total_NA = 0
        total_ED = 0
        total_MO = 0
        total_CC = 0
        total_SP = 0
        total_NE = 0
        total_ERROR = 0

        total_all = 0
        total_mo_all = 0
        total_ed_all = 0
        total_sp_all = 0
        total_na_all = 0

        for pr in self.pr_classifications:
            class_ = self.pr_classifications[pr]['class']
            if class_ == 'ED':
                total_ED += 1
            elif class_ == 'MO':
                total_MO += 1
            elif class_ == 'SP':
                total_SP += 1
            elif class_ == 'NA':
                total_NA += 1
            elif class_ == 'CC':
                total_CC += 1
            elif class_ == 'NE':
                total_NE += 1
            elif class_ == 'ERROR':
                total_ERROR += 1

            total_mid = total_MO + total_ED + total_SP
            total_all += total_mid

        total_total = len(self.prs)

        total_mo_all += total_MO
        total_ed_all += total_ED
        total_sp_all += total_SP
        total_na_all += total_NA

        totals_list = [total_MO, total_ED, total_SP, total_CC, total_NE, total_NA, total_ERROR]

        analysis.all_class_bar(totals_list, self.repo_check_number, self.repo_main_line, self.repo_divergent, True)

    def fetchPrData(self):
        destination_sha, self.ct = dataloader.getDestinationSha(self.repo_divergent, self.cut_off_date, self.token_list,
                                                                self.ct)
        self.ct, self.repo_data, req, runtime = dataloader.fetchPrData(self.repo_main_line, self.repo_divergent, self.prs,
                                                                       destination_sha, self.token_list, self.ct)

    def fetch_pullrequest_data(self):
        destination_sha, self.ct = dataloader.getDestinationSha(self.repo_divergent, self.cut_off_date, self.token_list, self.ct)
        self.ct, self.repo_data, req, runtime = dataloader.fetch_pullrequest_data(self.repo_main_line, self.repo_divergent,
                                                                                  self.prs, destination_sha,
                                                                                  self.token_list, self.ct, self.cut_off_date)
    def classify(self):
        print(f'\nStarting classification for {self.repo_main_line}, - , {self.repo_divergent}...')

        start = time.time()
        outputMO = 0
        outputED = 0
        outputSP = 0
        outputNA = 0
        for pr_nr in self.repo_data:
            if int(pr_nr) >= 0:
                try:
                    print(f'Currently Checking PR: {pr_nr}')
                    destination_sha = self.repo_data[pr_nr]['destination_sha']

                    self.results[pr_nr] = {}

                    dup_count = 1

                    for files in self.repo_data[pr_nr]['commits_data']:
                        for file in files:
                            self.results[pr_nr][file] = {}
                            if file.find(".") < 0:
                                result_mod = {}
                                self.results[pr_nr][file]['results'] = list()
                                result_mod['patchClass'] = 'OTHER EXT'
                                self.results[pr_nr][file]['result'] = result_mod
                                continue

                            file_ext = self.file_extensions_swapped.get("."+file.split('.')[1], "unknown")

                            if file_ext not in self.pareco_extensions:
                                result_mod = {}
                                self.results[pr_nr][file]['results'] = list()
                                result_mod['patchClass'] = 'OTHER EXT'
                                self.results[pr_nr][file]['result'] = result_mod
                                continue

                            if len(files[file]) != 0:
                                try:
                                    if file_ext != "unknown":
                                        parent = ''
                                        sha = ''
                                        fileName = ''
                                        fileDir = ''

                                        if len(files[file]) == 1:
                                            parent = files[file][0]['parent_sha']
                                            sha = files[file][0]['commit_sha']
                                            fileName = commitloader.fileName(file)
                                            fileDir = commitloader.fileDir(file)
                                            status = files[file][0]['status']
                                        else:
                                            first_commit, last_commit = classifier.getFirstLastCommit(
                                                self.repo_data[pr_nr]['commits_data'])
                                            parent = first_commit['parent_sha']
                                            sha = last_commit['commit_sha']
                                            fileName = commitloader.fileName(file)
                                            fileDir = commitloader.fileDir(file)
                                            status = first_commit['status']

                                        new_file_dir = ''
                                        for h in fileDir:
                                            new_file_dir = new_file_dir + h + '/'

                                        if self.ct == 40:
                                            self.ct = 0

                                        destPath, destUrl_ = classifier.getFileFromDest(self.repo_dir_files,
                                                                                        self.repo_divergent, destination_sha,
                                                                                        self.repo_check_number, file,
                                                                                        new_file_dir, fileName,
                                                                                        self.token_list[self.ct])

                                        self.ct += 1

                                        """
                                            Get the file after the patch from the variant1
                                        """
                                        if self.ct == 40:
                                            self.ct = 0

                                        fileAfterPatchDir, fileAfterPatchUrlAdd_ = classifier.getFileAfterPatch(
                                            self.repo_dir_files, self.repo_main_line, sha, self.repo_check_number, pr_nr, file,
                                            new_file_dir, fileName, self.token_list[self.ct])
                                        self.ct += 1

                                        patch_lines = files[file][0]['patch']
                                        patchPath = self.repo_dir_files + self.repo_check_number + '/' + self.repo_main_line + '/' + str(
                                            pr_nr) + '/patches/' + new_file_dir
                                        patchName = fileName.split('.')[0]
                                        patchPath, dup_count = classifier.save_patch(patchPath, patchName, patch_lines,
                                                                                     dup_count)

                                        shutil.copy(destPath, 'cmp/')
                                        shutil.copy(patchPath, 'src/')

                                        repo_files = patchPath.split('/')
                                        extension = destPath.split('.')[1]

                                        self.parse_patch_file(f'src/{repo_files[len(repo_files) - 1]}', f'src', f'{extension}')

                                        classification = ""
                                        tokens_jscpd = [50, 40, 30]
                                        MO_total = 0
                                        ED_total = 0
                                        SP_total = 0
                                        NA_total = 0
                                        for jscpdtoken in tokens_jscpd:
                                            MO_check = 0
                                            ED_check = 0
                                            SP_check = 0
                                            NA_check = 0
                                            test = subprocess.run(
                                                ['jscpd', '--pattern', f'*.{extension}', '--min-tokens',
                                                 f'{jscpdtoken}'])
                                            file_check = open('reports/html/jscpd-report.json')
                                            data_check = json.load(file_check)
                                            file_check.close()
                                            format = self.file_extensions_swapped.get("." + extension)
                                            try:
                                                for checks in data_check["statistics"]["formats"][format][
                                                    "sources"]:
                                                    if "deletions" in checks:
                                                        MO_check += \
                                                            data_check["statistics"]["formats"][format]["sources"][
                                                                checks]["duplicatedTokens"]
                                                    if "additions" in checks:
                                                        ED_check += \
                                                            data_check["statistics"]["formats"][format]["sources"][
                                                                checks]["duplicatedTokens"]
                                            except Exception as e:
                                                pass

                                            if MO_check == 0 and ED_check == 0:
                                                NA_check += 1
                                                continue
                                            elif MO_check == ED_check:
                                                SP_total += 1
                                                break
                                            elif MO_check > ED_check:
                                                MO_total += 1
                                                break
                                            elif ED_check > MO_check:
                                                ED_total += 1
                                                break

                                        self.remove_all_files('src')
                                        self.remove_all_files('cmp')
                                        self.remove_all_files('reports')

                                        if MO_total == 0 and ED_total == 0 and SP_total == 0:
                                            classification = "NA"
                                            outputNA += 1
                                        elif (SP_total > MO_total and SP_total > ED_total) or (MO_total == ED_total):
                                            classification = "SP"
                                            outputSP += 1
                                        elif MO_total > ED_total:
                                            classification = "MO"
                                            outputMO += 1
                                        elif ED_total > MO_total:
                                            classification = "ED"
                                            outputED += 1

                                        result_mod = {}
                                        result_mod['type'] = status.upper()
                                        result_mod['destPath'] = destPath
                                        result_mod['destUrl'] = destUrl_
                                        result_mod['fileAfterPatchUrl'] = fileAfterPatchUrlAdd_
                                        result_mod['fileBeforePatchUrl'] = ''
                                        result_mod['patchPath'] = patchPath
                                        result_mod['patchClass'] = classification

                                        self.results[pr_nr][file]['result'] = result_mod

                                    else:
                                        result_mod = {}
                                        result_mod['patchClass'] = 'OTHER EXT'
                                        self.results[pr_nr][file]['result'] = result_mod
                                except Exception as e:
                                    result_mod = {}
                                    result_mod['patchClass'] = 'ERROR'
                                    self.results[pr_nr][file]['result'] = result_mod
                                    print('Exception thrown is: ', e)
                                    print('File: ', file)
                                    exc_type, exc_obj, exc_tb = sys.exc_info()
                                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                    print(exc_type, fname, exc_tb.tb_lineno)
                            else:
                                result_mod = {}
                                self.results[pr_nr][file]['results'] = list()
                                if file_ext not in self.pareco_extensions:
                                    result_mod['patchClass'] = 'OTHER EXT'
                                    self.results[pr_nr][file]['result'] = result_mod
                                else:
                                    result_mod['patchClass'] = 'NOT EXISTING'
                                    self.results[pr_nr][file]['result'] = result_mod
                            # patch_lines = classifier.unified_diff(fileBeforePatchDir, emptyFilePath)
                            # patchPath = self.repo_dir_files + self.repo_file + '/' + self.variant1 + '/' + str(
                            #     pr_nr) + '/' + sha + '/patches/' + new_file_dir
                            # patchName = fileName.split('.')[0]
                            # patchPath, dup_count = classifier.save_patch(patchPath, patchName,
                            #                                              patch_lines, dup_count)
                    pass
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)

        self.pr_classifications = totals.final_class(self.results)
        all_counts = totals.count_all_classifications(self.pr_classifications)

        end = time.time()
        duration = end - start

        common.pickleFile(
            self.main_dir_results + self.repo_check_number + '_' + self.repo_main_line.split('/')[0] + '_' + self.repo_main_line.split('/')[
                1] + '_results', [self.results, self.pr_classifications, all_counts, duration])

    def runClassification(self, prs_source):
        self.set_prs(prs_source)
        self.fetchPrData()
        print('======================================================================')
        self.classify()
        self.createDf()
        print('======================================================================')
        self.visualizeResults()

    def dfPatches(self, nr_patches=-1):
        if nr_patches == -1:
            return self.df_patches
        else:
            if nr_patches > self.df_patches.shape[0]:
                print(
                    f'The dataframe contain only {self.df_patches.shape[0]} rows. Printing only {self.df_patches.shape[0]} rows.')
            return self.df_patches.head(nr_patches)

    def dfPatches(self, nr_patches=-1):
        if nr_patches == -1:
            return self.df_patches
        else:
            if nr_patches > self.df_patches.shape[0]:
                print(
                    f'The dataframe contain only {self.df_patches.shape[0]} rows. Printing only {self.df_patches.shape[0]} rows.')
            return self.df_patches.head(nr_patches)

    def dfFileClass(self, nr_patches=-1):
        if nr_patches == -1:
            return self.df_files_classes
        else:
            if nr_patches > self.df_files_classes.shape[0]:
                print(
                    f'The dataframe contain only {self.df_files_classes.shape[0]} rows. Printing only {self.df_files_classes.shape[0]} rows.')
            return self.df_files_classes.head(nr_patches)

    def dfPatchClass(self, nr_patches=-1):
        if nr_patches == -1:
            return self.df_patch_classes
        else:
            if nr_patches > self.df_patch_classes.shape[0]:
                print(
                    f'The dataframe contain only {self.df_patch_classes.shape[0]} rows. Printing only {self.df_patch_classes.shape[0]} rows.')
            return self.df_patch_classes.head(nr_patches)
