import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Set page configuration
st.set_page_config(
    page_title="Job Portal",
    page_icon="💼",
    layout="wide"
)

# Initialize session state for storing jobs if it doesn't exist
if 'jobs' not in st.session_state:
    # Check if we have a saved jobs file
    if os.path.exists('jobs.json'):
        with open('jobs.json', 'r') as f:
            st.session_state.jobs = json.load(f)
    else:
        # Sample job data
        st.session_state.jobs = [
            {
                "id": 1,
                "title": "Python Developer",
                "company": "Tech Solutions Inc.",
                "location": "San Francisco, CA",
                "salary": "$120,000 - $150,000",
                "description": "Looking for an experienced Python developer with knowledge of web frameworks.",
                "requirements": "5+ years of Python experience, Django/Flask, SQL",
                "date_posted": "2025-03-01",
                "contact_email": "jobs@techsolutions.com"
            },
            {
                "id": 2,
                "title": "Data Scientist",
                "company": "Data Insights Co.",
                "location": "Remote",
                "salary": "$130,000 - $160,000",
                "description": "Join our team to build machine learning models and analyze large datasets.",
                "requirements": "ML experience, Python, SQL, Statistics background",
                "date_posted": "2025-03-05",
                "contact_email": "careers@datainsights.com"
            },
            {
                "id": 3,
                "title": "Frontend Developer",
                "company": "WebUI Experts",
                "location": "New York, NY",
                "salary": "$110,000 - $140,000",
                "description": "Create responsive and interactive user interfaces for our clients.",
                "requirements": "React, JavaScript, HTML/CSS, 3+ years experience",
                "date_posted": "2025-03-08",
                "contact_email": "hr@webuiexperts.com"
            }
        ]

# Function to save jobs to file
def save_jobs():
    with open('jobs.json', 'w') as f:
        json.dump(st.session_state.jobs, f)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Browse Jobs", "Post a Job"])

# Browse Jobs Page
if page == "Browse Jobs":
    st.title("🔍 Browse Available Jobs")
    
    # Search and filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("Search by keyword")
    with col2:
        locations = ["All Locations"] + list(set(job["location"] for job in st.session_state.jobs))
        location_filter = st.selectbox("Filter by location", locations)
    with col3:
        sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Company A-Z"])
    
    # Filter jobs based on search and filters
    filtered_jobs = st.session_state.jobs.copy()
    
    if search_term:
        filtered_jobs = [job for job in filtered_jobs if 
                        search_term.lower() in job["title"].lower() or 
                        search_term.lower() in job["description"].lower() or
                        search_term.lower() in job["company"].lower()]
    
    if location_filter != "All Locations":
        filtered_jobs = [job for job in filtered_jobs if job["location"] == location_filter]
    
    # Sort jobs
    if sort_by == "Newest First":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x["date_posted"], reverse=True)
    elif sort_by == "Oldest First":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x["date_posted"])
    elif sort_by == "Company A-Z":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x["company"])
    
    # Display job count
    st.write(f"Found {len(filtered_jobs)} jobs")
    
    # Display jobs
    for job in filtered_jobs:
        with st.expander(f"{job['title']} at {job['company']} - {job['location']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(job["title"])
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")
                st.write(f"**Salary:** {job['salary']}")
                st.write("**Description:**")
                st.write(job["description"])
                st.write("**Requirements:**")
                st.write(job["requirements"])
            with col2:
                st.write(f"**Posted:** {job['date_posted']}")
                st.write(f"**Contact:** {job['contact_email']}")
                if st.button("Apply Now", key=f"apply_{job['id']}"):
                    st.info(f"To apply, please send your resume to {job['contact_email']}")

# Post a Job Page
elif page == "Post a Job":
    st.title("📝 Post a New Job")
    
    with st.form("job_form"):
        job_title = st.text_input("Job Title*")
        company = st.text_input("Company Name*")
        location = st.text_input("Location*")
        salary = st.text_input("Salary Range")
        description = st.text_area("Job Description*")
        requirements = st.text_area("Requirements*")
        contact_email = st.text_input("Contact Email*")
        
        submitted = st.form_submit_button("Post Job")
        
        if submitted:
            if job_title and company and location and description and requirements and contact_email:
                # Create new job entry
                new_job = {
                    "id": len(st.session_state.jobs) + 1,
                    "title": job_title,
                    "company": company,
                    "location": location,
                    "salary": salary if salary else "Not specified",
                    "description": description,
                    "requirements": requirements,
                    "date_posted": datetime.now().strftime("%Y-%m-%d"),
                    "contact_email": contact_email
                }
                
                # Add to jobs list
                st.session_state.jobs.append(new_job)
                save_jobs()
                
                st.success("Job posted successfully!")
                st.balloons()
            else:
                st.error("Please fill in all required fields marked with *")

# Footer
st.markdown("---")
st.markdown("© 2025 Job Portal App | Built with Streamlit")

# Display the current jobs data for debugging (can be removed in production)
if st.sidebar.checkbox("Show raw data (Admin)"):
    st.sidebar.write(st.session_state.jobs)