## **Instructions when setting up the webpage with autofetching Google Scholar on a new laptop:**


### ✅ **What stays the same (no changes needed):**
- **All your scripts** (`update_publications_manual.sh`, `scholar_sync.py`, etc.)
- **Your Google Scholar ID** (in `config.json`)
- **Your publication data** (all in git)
- **Your website** (hosted on GitHub Pages)

### �� **What you need to install on the new laptop:**

1. **Python 3.9+** (for the scripts)
2. **Chrome browser** (for Selenium web scraping)
3. **Git** (to access your repository)

### 📋 **Setup steps on new laptop:**

1. **Clone your repository:**
   ```bash
   git clone https://github.com/amritamwebpage/amritamwebpage.github.io.git
   cd amritamwebpage.github.io
   ```

2. **Install Python dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Create the alias again:**
   ```bash
   echo 'alias update-pubs="cd /path/to/your/website && ./update_publications_manual.sh"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Test it:**
   ```bash
   update-pubs
   ```

### 🎯 **That's it!** 

**Everything else is automatic:**
- ✅ Scripts work the same
- ✅ Your Google Scholar ID stays the same
- ✅ Your website updates the same way
- ✅ All your publication data is preserved
