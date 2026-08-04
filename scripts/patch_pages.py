import os
import glob

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched
    if "try:" in content and "except Exception as e:" in content and "app_logger.error" in content:
        return
        
    lines = content.split('\n')
    
    # Find where the imports and initial setup end (e.g. after section_title)
    insert_idx = -1
    for i, line in enumerate(lines):
        if "section_title" in line or "st.title(" in line or "inject_global_css" in line:
            insert_idx = i
            
    if insert_idx == -1:
        # Fallback to after set_page_config
        for i, line in enumerate(lines):
            if "st.set_page_config" in line:
                insert_idx = i
                
    if insert_idx == -1:
        insert_idx = 0
        
    insert_idx += 1
    
    # We will wrap everything after insert_idx
    new_lines = lines[:insert_idx]
    new_lines.append("")
    new_lines.append("try:")
    
    for line in lines[insert_idx:]:
        new_lines.append("    " + line if line.strip() else line)
        
    new_lines.append("")
    new_lines.append("except Exception as e:")
    new_lines.append("    import traceback")
    new_lines.append("    import sys")
    new_lines.append("    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))")
    new_lines.append("    from utils.logger import app_logger")
    new_lines.append("    app_logger.error(f'Error in {os.path.basename(filepath)}: {str(e)}\\n{traceback.format_exc()}')")
    new_lines.append("    st.error('An unexpected error occurred while loading this page.')")
    new_lines.append("    with st.expander('View Technical Details'):")
    new_lines.append("        st.code(traceback.format_exc())")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    pages = glob.glob(r"d:\antigravity project\CLT_Mission\AI_Career_Intelligence_Platform\app\pages\*.py")
    for page in pages:
        patch_file(page)
    print("Patched all pages successfully.")
