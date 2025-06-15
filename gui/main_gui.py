import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import subprocess
import platform
import webbrowser
from typing import List, Dict
import json
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Check for required imports
try:
    from database import DatabaseConnection
    from src.cv_matcher import CVMatcher
    from src.ekstrak_regex import extract_details_regex, extract_regex
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all required files are present and dependencies are installed.")
    print("Run 'python scripts/setup.py' to install dependencies.")
    sys.exit(1)

class ATSApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("ATS - Applicant Tracking System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
          # Initialize components
        self.db = DatabaseConnection()
        self.cv_matcher = CVMatcher()
        self.current_results = []
        self.timing_info = {}
        
        # Check database connection
        if not self.db.is_connected():
            messagebox.showwarning("Database Warning", 
                "Database connection failed. Running in demo mode with sample data.")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="ATS - Applicant Tracking System", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Search Configuration", padding="15")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)
        
        # Keywords input
        ttk.Label(input_frame, text="Keywords (comma-separated):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.keywords_entry = ttk.Entry(input_frame, font=("Arial", 11))
        self.keywords_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(10, 0))
        self.keywords_entry.insert(0, "python, react, sql")  # Default keywords
          # Algorithm selection with better styling
        ttk.Label(input_frame, text="Pattern Matching Algorithm:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        algorithm_frame = ttk.LabelFrame(input_frame, text="Algorithm Selection", padding="10")
        algorithm_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(10, 5), padx=(10, 0))
        
        self.algorithm_var = tk.StringVar(value="kmp")
        
        # KMP Radio Button with description
        kmp_frame = ttk.Frame(algorithm_frame)
        kmp_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Radiobutton(kmp_frame, text="KMP (Knuth-Morris-Pratt)", 
                       variable=self.algorithm_var, value="kmp").pack(side=tk.LEFT)
        ttk.Label(kmp_frame, text="- Linear time O(n+m)", 
                 font=("Arial", 9), foreground="gray").pack(side=tk.LEFT, padx=(10, 0))
        
        # Boyer-Moore Radio Button with description
        bm_frame = ttk.Frame(algorithm_frame)
        bm_frame.pack(fill=tk.X)
        ttk.Radiobutton(bm_frame, text="BM (Boyer-Moore)", 
                       variable=self.algorithm_var, value="boyer_moore").pack(side=tk.LEFT)
        ttk.Label(bm_frame, text="- Efficient for large texts", 
                 font=("Arial", 9), foreground="gray").pack(side=tk.LEFT, padx=(10, 0))
          # Top matches selector with better labeling
        ttk.Label(input_frame, text="Number of Top Results:").grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        top_matches_frame = ttk.Frame(input_frame)
        top_matches_frame.grid(row=2, column=1, sticky=tk.W, pady=(15, 5), padx=(10, 0))
        
        self.top_matches_var = tk.StringVar(value="10")
        top_matches_combo = ttk.Combobox(top_matches_frame, textvariable=self.top_matches_var, 
                                       values=["5", "10", "15", "20", "25", "30", "All"], 
                                       width=8, state="readonly")
        top_matches_combo.pack(side=tk.LEFT)
        ttk.Label(top_matches_frame, text="matches to display", 
                 font=("Arial", 9), foreground="gray").pack(side=tk.LEFT, padx=(5, 0))
        
        # Fuzzy matching threshold
        ttk.Label(input_frame, text="Fuzzy Match Threshold:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        threshold_frame = ttk.Frame(input_frame)
        threshold_frame.grid(row=3, column=1, sticky=tk.W, pady=(10, 5), padx=(10, 0))
        
        self.threshold_var = tk.DoubleVar(value=0.7)
        threshold_scale = ttk.Scale(threshold_frame, from_=0.1, to=1.0, 
                                  variable=self.threshold_var, orient=tk.HORIZONTAL, length=200)
        threshold_scale.pack(side=tk.LEFT)
        self.threshold_label = ttk.Label(threshold_frame, text=f"{self.threshold_var.get():.1f}")
        self.threshold_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Update threshold label when scale changes
        def update_threshold_label(*args):
            self.threshold_label.config(text=f"{self.threshold_var.get():.1f}")
        self.threshold_var.trace('w', update_threshold_label)
          # Search button with enhanced styling
        search_btn = ttk.Button(input_frame, text="🔍 Search CVs", command=self.search_cvs, 
                               style="Accent.TButton")
        search_btn.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        # Clear button
        clear_btn = ttk.Button(input_frame, text="🗑️ Clear Results", command=self.clear_results)
        clear_btn.grid(row=4, column=1, sticky=tk.E, pady=(20, 0), padx=(10, 0))
        
        # Results Section
        results_frame = ttk.LabelFrame(main_frame, text="Search Results", padding="15")
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
          # Performance metrics section
        performance_frame = ttk.LabelFrame(results_frame, text="Performance Metrics", padding="10")
        performance_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        performance_frame.columnconfigure(1, weight=1)
        
        # Performance labels
        ttk.Label(performance_frame, text="Algorithm Used:", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.algorithm_used_label = ttk.Label(performance_frame, text="None", font=("Arial", 9))
        self.algorithm_used_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(performance_frame, text="Exact Match Time:", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        self.exact_time_label = ttk.Label(performance_frame, text="0.000s", font=("Arial", 9))
        self.exact_time_label.grid(row=0, column=3, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(performance_frame, text="Fuzzy Match Time:", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky=tk.W)
        self.fuzzy_time_label = ttk.Label(performance_frame, text="0.000s", font=("Arial", 9))
        self.fuzzy_time_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(performance_frame, text="CVs Processed:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        self.cvs_processed_label = ttk.Label(performance_frame, text="0", font=("Arial", 9))
        self.cvs_processed_label.grid(row=1, column=3, sticky=tk.W, padx=(10, 0))
        
        # Results summary section
        self.summary_label = ttk.Label(results_frame, text="No search performed yet.", 
                                      font=("Arial", 11), foreground="gray")
        self.summary_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 10))
          # Results treeview with enhanced columns
        columns = ("Rank", "Name", "Role", "Exact Matches", "Fuzzy Matches", "Total Score", "Match Details")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=12)
        
        # Configure column headings and widths
        self.results_tree.heading("Rank", text="Rank")
        self.results_tree.heading("Name", text="Applicant Name")
        self.results_tree.heading("Role", text="Position")
        self.results_tree.heading("Exact Matches", text="Exact Matches")
        self.results_tree.heading("Fuzzy Matches", text="Fuzzy Matches")
        self.results_tree.heading("Total Score", text="Total Score")
        self.results_tree.heading("Match Details", text="Keywords Found")
        
        self.results_tree.column("Rank", width=50)
        self.results_tree.column("Name", width=180)
        self.results_tree.column("Role", width=120)
        self.results_tree.column("Exact Matches", width=100)
        self.results_tree.column("Fuzzy Matches", width=100)
        self.results_tree.column("Total Score", width=90)
        self.results_tree.column("Match Details", width=250)
        
        # Grid the treeview
        self.results_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars for treeview
        scrollbar_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        scrollbar_y.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.results_tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        scrollbar_x.grid(row=3, column=0, sticky=(tk.W, tk.E))
        self.results_tree.configure(xscrollcommand=scrollbar_x.set)
        
        # Action buttons
        action_frame = ttk.Frame(results_frame)
        action_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(action_frame, text="📄 View Summary", 
                  command=self.view_summary).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="📋 View Full CV", 
                  command=self.view_full_cv).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="📊 Export Results", 
                  command=self.export_results).pack(side=tk.LEFT)
        
        # Configure styles
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 11, "bold"))
    def search_cvs(self):
        """Perform CV search based on user input"""
        keywords_text = self.keywords_entry.get().strip()
        if not keywords_text:
            messagebox.showwarning("Input Error", "Please enter keywords to search.")
            return
        
        keywords = [kw.strip().lower() for kw in keywords_text.split(",") if kw.strip()]
        algorithm = self.algorithm_var.get()
        
        # Get top matches setting
        top_matches_text = self.top_matches_var.get()
        if top_matches_text.lower() == "all":
            top_matches = None
        else:
            try:
                top_matches = int(top_matches_text)
            except ValueError:
                top_matches = 10
        
        # Update CV matcher threshold
        self.cv_matcher.similarity_threshold = self.threshold_var.get()
        
        # Get all CV data from database
        cv_data_list = self.db.get_all_applicants()
        if not cv_data_list:
            messagebox.showinfo("No Data", "No CV data found in the database.")
            return
        
        # Show loading message
        self.summary_label.config(text="🔍 Searching CVs... Please wait.")
        self.root.update()
        
        try:
            # Perform enhanced search with ranking
            results, timing_info = self.cv_matcher.search_cvs(cv_data_list, keywords, algorithm, top_matches)
            
            # Store results and timing
            self.current_results = results
            self.timing_info = timing_info
            
            # Update UI displays
            self.update_results_display()
            self.update_performance_display()
            
        except Exception as e:
            messagebox.showerror("Search Error", f"An error occurred during search: {str(e)}")
            self.summary_label.config(text="❌ Search failed.")
            print(f"Search error details: {e}")  # For debugging
    def update_results_display(self):
        """Update the results treeview with enhanced information"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add new results with ranking
        for i, result in enumerate(self.current_results, 1):
            cv_data = result['cv_data']
            name = f"{cv_data.get('name', cv_data.get('first_name', 'Unknown'))}"
            if cv_data.get('last_name'):
                name += f" {cv_data['last_name']}"
            
            role = cv_data.get('position', cv_data.get('application_role', 'N/A'))
            exact_matches = result['exact_score']
            fuzzy_matches = result['fuzzy_score']
            total_score = f"{result['total_score']:.1f}"
            
            # Create keywords found summary
            keywords_found = []
            if result.get('exact_matches'):
                keywords_found.extend(result['exact_matches'].keys())
            if result.get('fuzzy_matches'):
                keywords_found.extend([k for k, v in result['fuzzy_matches'].items() if v])
            
            match_details = ', '.join(keywords_found[:3])  # Show first 3 keywords
            if len(keywords_found) > 3:
                match_details += f" (+{len(keywords_found)-3} more)"
            
            # Add alternating row colors
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            
            self.results_tree.insert("", tk.END, values=(
                f"#{i}", name, role, exact_matches, fuzzy_matches, total_score, match_details
            ), tags=(tag,))
        
        # Configure row colors
        self.results_tree.tag_configure("evenrow", background="#f8f9fa")
        self.results_tree.tag_configure("oddrow", background="#ffffff")
    
    def update_summary_display(self):
        """Update the summary display"""
        if not self.timing_info:
            return
        
        exact_time = self.timing_info['exact_match_time']
        fuzzy_time = self.timing_info['fuzzy_match_time']
        total_cvs = self.timing_info['total_cvs_scanned']
        algorithm = self.timing_info['algorithm_used']
        
        summary_text = f"Exact Match ({algorithm}): {total_cvs} CVs scanned in {exact_time:.1f}ms"
        if fuzzy_time > 0:
            summary_text += f"\nFuzzy Match: {total_cvs} CVs scanned in {fuzzy_time:.1f}ms"
        
        self.summary_label.config(text=summary_text)
    
    def get_selected_result(self):
        """Get the currently selected result"""
        selection = self.results_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a CV from the results.")
            return None
        
        item = self.results_tree.item(selection[0])
        row_index = self.results_tree.index(selection[0])
        
        if row_index < len(self.current_results):
            return self.current_results[row_index]
        return None
    
    def view_summary(self):
        """Display CV summary in a new window"""
        result = self.get_selected_result()
        if not result:
            return
        
        cv_data = result['cv_data']
        cv_path = cv_data['cv_path']
        
        # Extract CV text and details
        cv_text = self.cv_matcher.extract_cv_text(cv_path)
        if not cv_text:
            messagebox.showerror("Error", "Could not extract text from CV.")
            return
        
        cv_details = extract_details_regex(cv_text)
        
        # Create summary window
        summary_window = tk.Toplevel(self.root)
        summary_window.title(f"CV Summary - {cv_data['first_name']} {cv_data['last_name'] or ''}")
        summary_window.geometry("800x600")
        
        # Summary content
        summary_frame = ttk.Frame(summary_window, padding="20")
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        # Personal Information
        personal_frame = ttk.LabelFrame(summary_frame, text="Personal Information", padding="10")
        personal_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(personal_frame, text=f"Name: {cv_data['first_name']} {cv_data['last_name'] or ''}").pack(anchor=tk.W)
        if cv_data['phone_number']:
            ttk.Label(personal_frame, text=f"Phone: {cv_data['phone_number']}").pack(anchor=tk.W)
        if cv_data['email']:
            ttk.Label(personal_frame, text=f"Email: {cv_data['email']}").pack(anchor=tk.W)
        if cv_data['address']:
            ttk.Label(personal_frame, text=f"Address: {cv_data['address']}").pack(anchor=tk.W)
        ttk.Label(personal_frame, text=f"Application Role: {cv_data['application_role']}").pack(anchor=tk.W)
        
        # CV Details in scrolled text
        details_frame = ttk.LabelFrame(summary_frame, text="CV Details", padding="10")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        details_text = scrolledtext.ScrolledText(details_frame, height=20, width=80)
        details_text.pack(fill=tk.BOTH, expand=True)
        
        # Format CV details
        formatted_details = self.format_cv_details(cv_details, result)
        details_text.insert(tk.END, formatted_details)
        details_text.config(state=tk.DISABLED)
        
        # Action buttons
        button_frame = ttk.Frame(summary_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="View Full CV", 
                  command=lambda: self.open_cv_file(cv_path)).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Close", 
                  command=summary_window.destroy).pack(side=tk.RIGHT)
    
    def format_cv_details(self, cv_details, result):
        """Format CV details for display"""
        formatted = ""
        
        # Add match information
        formatted += "=== KEYWORD MATCHES ===\n"
        if result['exact_matches']:
            formatted += "Exact Matches:\n"
            for keyword, match_info in result['exact_matches'].items():
                formatted += f"  • {keyword}: {match_info['count']} occurrences\n"
        
        if result['fuzzy_matches']:
            formatted += "\nFuzzy Matches:\n"
            for keyword, matches in result['fuzzy_matches'].items():
                formatted += f"  • {keyword}:\n"
                for match in matches[:3]:  # Show top 3 fuzzy matches
                    formatted += f"    - {match['word']} (similarity: {match['similarity']:.2f})\n"
        
        formatted += "\n=== CV CONTENT ===\n"
        
        # Summary
        if cv_details['summary']:
            formatted += "SUMMARY:\n"
            for item in cv_details['summary']:
                formatted += f"  {item}\n"
            formatted += "\n"
        
        # Skills
        if cv_details['skills']:
            formatted += "SKILLS:\n"
            for skill in cv_details['skills']:
                formatted += f"  • {skill}\n"
            formatted += "\n"
        
        # Experience
        if cv_details['experience']:
            formatted += "EXPERIENCE:\n"
            for exp in cv_details['experience']:
                formatted += f"  Period: {exp['periode']}\n"
                formatted += f"  Position: {exp['info_jabatan']}\n"
                if exp['deskripsi']:
                    formatted += "  Description:\n"
                    for desc in exp['deskripsi']:
                        formatted += f"    - {desc}\n"
                formatted += "\n"
        
        # Education
        if cv_details['education']:
            formatted += "EDUCATION:\n"
            for edu in cv_details['education']:
                formatted += f"  • {edu}\n"
        
        return formatted
    
    def view_full_cv(self):
        """Open the full CV file"""
        result = self.get_selected_result()
        if not result:
            return
        
        cv_path = result['cv_data']['cv_path']
        self.open_cv_file(cv_path)
    
    def open_cv_file(self, cv_path):
        """Open CV file with default application"""
        if not os.path.exists(cv_path):
            messagebox.showerror("File Error", f"CV file not found: {cv_path}")
            return
        
        try:
            if platform.system() == 'Windows':
                os.startfile(cv_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', cv_path])
            else:  # Linux
                subprocess.run(['xdg-open', cv_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open CV file: {str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        self.db.disconnect()
        self.root.destroy()
    
    def clear_results(self):
        """Clear all search results"""
        # Clear treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Reset labels
        self.summary_label.config(text="No search performed yet.")
        self.algorithm_used_label.config(text="None")
        self.exact_time_label.config(text="0.000s")
        self.fuzzy_time_label.config(text="0.000s")
        self.cvs_processed_label.config(text="0")
        
        # Clear internal data
        self.current_results = []
        self.timing_info = {}
    
    def export_results(self):
        """Export search results to CSV"""
        if not self.current_results:
            messagebox.showwarning("No Results", "No search results to export.")
            return
        
        try:
            from tkinter.filedialog import asksaveasfilename
            import csv
            
            filename = asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save Search Results"
            )
            
            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow(['Rank', 'Name', 'Position', 'Email', 'Phone', 
                                   'Exact Matches', 'Fuzzy Matches', 'Total Score', 'Keywords Found'])
                    
                    # Write data
                    for i, result in enumerate(self.current_results, 1):
                        cv_data = result['cv_data']
                        name = f"{cv_data['first_name']} {cv_data['last_name'] or ''}".strip()
                        
                        # Get keywords found
                        keywords_found = []
                        if result['exact_matches']:
                            keywords_found.extend(result['exact_matches'].keys())
                        if result['fuzzy_matches']:
                            keywords_found.extend(result['fuzzy_matches'].keys())
                        
                        writer.writerow([
                            i, name, cv_data.get('application_role', 'N/A'),
                            cv_data.get('email', ''), cv_data.get('phone_number', ''),
                            result['exact_score'], result['fuzzy_score'], 
                            f"{result['total_score']:.1f}", ', '.join(keywords_found)
                        ])
                
                messagebox.showinfo("Export Complete", f"Results exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")

    def update_performance_display(self):
        """Update performance metrics display"""
        if not self.timing_info:
            return
        
        # Update performance labels
        algorithm = self.timing_info.get('algorithm_used', 'None')
        exact_time = self.timing_info.get('exact_match_time', 0)
        fuzzy_time = self.timing_info.get('fuzzy_match_time', 0)
        total_cvs = self.timing_info.get('total_cvs_scanned', 0)
        
        self.algorithm_used_label.config(text=algorithm.upper())
        self.exact_time_label.config(text=f"{exact_time:.3f}s")
        self.fuzzy_time_label.config(text=f"{fuzzy_time:.3f}s")
        self.cvs_processed_label.config(text=str(total_cvs))
        
        # Update summary
        total_results = len(self.current_results)
        summary_text = f"Found {total_results} matching CVs from {total_cvs} processed"
        if exact_time > 0 or fuzzy_time > 0:
            total_time = exact_time + fuzzy_time
            summary_text += f" | Total processing time: {total_time:.3f}s"
        
        self.summary_label.config(text=summary_text)

def main():
    root = tk.Tk()
    app = ATSApplication(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
