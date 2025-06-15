"""
Sample CV Generator for Testing ATS System
Creates sample PDF CVs with various skills and experiences
"""

import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from faker import Faker
import random

fake = Faker()

# Sample data for different roles
ROLE_SKILLS = {
    'HR': [
        'recruitment', 'talent acquisition', 'employee relations', 'performance management',
        'compensation', 'benefits administration', 'training', 'development', 'HR analytics',
        'employment law', 'organizational development', 'conflict resolution'
    ],
    'Designer': [
        'photoshop', 'illustrator', 'figma', 'sketch', 'adobe creative suite', 'ui design',
        'ux design', 'web design', 'graphic design', 'branding', 'typography', 'color theory',
        'wireframing', 'prototyping', 'user research'
    ],
    'Engineer': [
        'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mongodb', 'aws',
        'docker', 'kubernetes', 'git', 'agile', 'scrum', 'microservices', 'rest api',
        'machine learning', 'data structures', 'algorithms'
    ],
    'Marketing': [
        'digital marketing', 'social media', 'content marketing', 'seo', 'sem', 'ppc',
        'email marketing', 'marketing automation', 'analytics', 'brand management',
        'campaign management', 'market research', 'customer segmentation'
    ],
    'Sales': [
        'sales strategy', 'lead generation', 'customer relationship management', 'crm',
        'negotiation', 'closing', 'prospecting', 'cold calling', 'sales presentations',
        'account management', 'business development', 'sales forecasting'
    ]
}

EXPERIENCE_TEMPLATES = {
    'HR': [
        'Managed recruitment process for {} positions',
        'Developed employee training programs',
        'Implemented performance management system',
        'Handled employee relations and conflict resolution'
    ],
    'Designer': [
        'Created {} design concepts for various clients',
        'Designed user interfaces for web and mobile applications',
        'Developed brand identity and marketing materials',
        'Collaborated with development teams on UI/UX implementation'
    ],
    'Engineer': [
        'Developed {} applications using modern technologies',
        'Implemented microservices architecture',
        'Optimized database performance and scalability',
        'Led technical design and code reviews'
    ],
    'Marketing': [
        'Managed {} marketing campaigns with {}% ROI',
        'Increased social media engagement by {}%',
        'Developed content strategy and marketing materials',
        'Analyzed market trends and customer behavior'
    ],
    'Sales': [
        'Achieved {}% of sales targets consistently',
        'Generated ${} in revenue through new client acquisition',
        'Managed portfolio of {} key accounts',
        'Developed sales strategies and presentations'
    ]
}

def generate_cv_content(role):
    """Generate CV content for a specific role"""
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    address = fake.address().replace('\n', ', ')
    
    # Generate skills
    role_skills = ROLE_SKILLS.get(role, [])
    skills = random.sample(role_skills, min(8, len(role_skills)))
    
    # Generate experience
    experiences = []
    for i in range(random.randint(2, 4)):
        company = fake.company()
        position = f"{role} {random.choice(['Specialist', 'Manager', 'Lead', 'Senior', 'Associate'])}"
        start_date = fake.date_between(start_date='-8y', end_date='-2y')
        end_date = fake.date_between(start_date=start_date, end_date='today')
        
        # Generate experience descriptions
        templates = EXPERIENCE_TEMPLATES.get(role, ['Performed various tasks related to the role'])
        descriptions = []
        for _ in range(random.randint(2, 4)):
            template = random.choice(templates)
            if '{}' in template:
                if 'positions' in template:
                    desc = template.format(random.randint(10, 50))
                elif 'applications' in template:
                    desc = template.format(random.randint(5, 20))
                elif 'campaigns' in template:
                    desc = template.format(random.randint(3, 15), random.randint(15, 45))
                elif 'engagement' in template:
                    desc = template.format(random.randint(20, 80))
                elif 'targets' in template:
                    desc = template.format(random.randint(95, 120))
                elif 'revenue' in template:
                    desc = template.format(f"{random.randint(100, 500)}K")
                elif 'accounts' in template:
                    desc = template.format(random.randint(15, 50))
                elif 'design concepts' in template:
                    desc = template.format(random.randint(50, 200))
                else:
                    desc = template.format(random.randint(5, 25))
            else:
                desc = template
            descriptions.append(desc)
        
        experiences.append({
            'period': f"{start_date.strftime('%m/%Y')} - {end_date.strftime('%m/%Y')}",
            'position': position,
            'company': company,
            'descriptions': descriptions
        })
    
    # Generate education
    education = []
    for _ in range(random.randint(1, 2)):
        degree = random.choice(['Bachelor', 'Master', 'Associate'])
        field = random.choice(['Computer Science', 'Business Administration', 'Marketing', 'Design', 'Engineering'])
        university = fake.company() + ' University'
        grad_date = fake.date_between(start_date='-15y', end_date='-5y')
        education.append(f"{degree} of {field}, {university} ({grad_date.strftime('%Y')})")
    
    # Generate summary
    summary_templates = [
        f"Experienced {role.lower()} professional with {random.randint(3, 10)} years of experience",
        f"Results-driven {role.lower()} specialist with proven track record",
        f"Dedicated {role.lower()} professional passionate about delivering excellence"
    ]
    summary = random.choice(summary_templates)
    
    return {
        'name': name,
        'email': email,
        'phone': phone,
        'address': address,
        'summary': summary,
        'skills': skills,
        'experience': experiences,
        'education': education
    }

def create_cv_pdf(cv_data, output_path):
    """Create a PDF CV from the generated data"""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    
    # Name and contact info
    story.append(Paragraph(cv_data['name'], title_style))
    story.append(Paragraph(f"Email: {cv_data['email']} | Phone: {cv_data['phone']}", styles['Normal']))
    story.append(Paragraph(f"Address: {cv_data['address']}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("Summary", heading_style))
    story.append(Paragraph(cv_data['summary'], styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Skills
    story.append(Paragraph("Skills", heading_style))
    skills_text = " • ".join(cv_data['skills'])
    story.append(Paragraph(skills_text, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Experience
    story.append(Paragraph("Experience", heading_style))
    for exp in cv_data['experience']:
        story.append(Paragraph(f"<b>{exp['period']}</b>", styles['Normal']))
        story.append(Paragraph(f"<b>{exp['position']}</b> - {exp['company']}", styles['Normal']))
        for desc in exp['descriptions']:
            story.append(Paragraph(f"• {desc}", styles['Normal']))
        story.append(Spacer(1, 10))
    
    # Education
    story.append(Paragraph("Education", heading_style))
    for edu in cv_data['education']:
        story.append(Paragraph(f"• {edu}", styles['Normal']))
    
    doc.build(story)

def generate_sample_cvs(num_cvs_per_role=5):
    """Generate sample CVs for all roles"""
    base_path = "data"
    
    for role in ROLE_SKILLS.keys():
        role_path = os.path.join(base_path, role)
        os.makedirs(role_path, exist_ok=True)
        
        print(f"Generating {num_cvs_per_role} CVs for {role}...")
        
        for i in range(num_cvs_per_role):
            cv_data = generate_cv_content(role)
            filename = f"{role.lower()}_{i+1:02d}.pdf"
            output_path = os.path.join(role_path, filename)
            
            try:
                create_cv_pdf(cv_data, output_path)
                print(f"  Created: {filename}")
            except Exception as e:
                print(f"  Error creating {filename}: {e}")

if __name__ == "__main__":
    # Install required package if not available
    try:
        import reportlab
    except ImportError:
        print("Installing reportlab...")
        import subprocess
        subprocess.check_call(["pip", "install", "reportlab"])
        import reportlab
    
    generate_sample_cvs(10)  # Generate 10 CVs per role
    print("Sample CV generation completed!")
