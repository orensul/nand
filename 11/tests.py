import os
import sys
fmt_diff = 'diff -w {0} {1}'
fmt_echo = 'echo {0}'
if __name__ == '__main__':
    input_str = sys.argv[1]
    summary = []
    if os.path.isdir(input_str):
        for filename in os.listdir(sys.argv[1]):
            if filename.endswith("A.vm") and not (filename.startswith('Array.vm') or
            filename.startswith('Keyboard.vm') or filename.startswith('Math.vm')
                                                 or filename.startswith('Math.vm')
                                                 or filename.startswith('Memory.vm')
                                                 or filename.startswith('Output.vm')
                                                 or filename.startswith('Screen.vm')
                                                 or filename.startswith('String.vm')
                                                 or filename.startswith('Sys.vm')):

                ref_path = os.path.join(sys.argv[1], filename)
                res_path = os.path.join(sys.argv[1],
                                        filename.replace('A.vm', '.vm'))
                res_diff = os.system(fmt_diff.format(ref_path, res_path))
                if res_diff != 0:
                    summary.append(filename)
        print("Summary: " + str(len(summary)) + " tests failed\n")
        for file_n in summary:
            print("In file: " + file_n + " there were diffs\n")
    else:
        print("No directory was found")
