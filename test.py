import os

def print_tree(start_path='.', indent=''):
    for root, dirs, files in os.walk(start_path):
        level = root.replace(start_path, '').count(os.sep)
        indent_space = '    ' * level
        print(f"{indent_space}{os.path.basename(root)}/")
        sub_indent = '    ' * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")

print_tree('.')  
