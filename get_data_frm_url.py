import csv
from playwright.sync_api import sync_playwright

output_file = "student_full_data.csv"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto("https://payonline.narayanagroup.com/?_gl=1*1sl6clz*_gcl_au*NTU0MTQ0MDY1LjE3NTE1NjIyODI.")  # replace with actual URL

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Student Number", "Mobile Number" ,"Student Name", "Father Name", "Mother Name",
            "Branch Name", "Class Name", "Course Amount", "Due Amount"
        ])

        # for stdnm in range(6000000, 6142980):  # Adjust range as needed
        for stdnm in range(6055000, 6142980):  # Adjust range as needed
            student_number = str(stdnm)
            print("Student Number:", student_number)

            page.fill('input[formcontrolname="txtStudentNumber"]', '')  # Clear
            page.fill('input[formcontrolname="txtStudentNumber"]', student_number)
            page.click('button.btn >> i.fa-search')
            page.wait_for_selector('input[formcontrolname="studentName"]', timeout=3000)

            # Check for "Student not found"
            if page.locator('span.text-danger', has_text="Student not found").is_visible():
                print(f"{student_number} -> Student not found")
                writer.writerow([student_number, "Not Found", "", "", "", "", "", ""])
                continue
            def get_value(formcontrol):
                try:
                    return page.locator(f'input[formcontrolname="{formcontrol}"]').evaluate("el => el.value")
                except:
                    return "Not Found"


            studentNamevalue = get_value("studentName")
            mobileNumbervalue = get_value("mobileNumber")
            fatherNamevalue = get_value("fatherName")
            motherNamevalue = get_value("motherName")
            branchNamevalue = get_value("branchName")
            classNamevalue = get_value("className")
            courseAmountvalue = get_value("courseAmount")
            dueAmountvalue = get_value("dueAmount")
            #
            # print("Student Name:", studentNamevalue)
            # print("Mobile Number", mobileNumbervalue)
            # print("Father Name:", fatherNamevalue)
            # print("Mother Name:", motherNamevalue)
            # print("Branch Name:", branchNamevalue)
            # print("Class Name:", classNamevalue)
            # print("Course Amount:", courseAmountvalue)
            # print("Due Amount:", dueAmountvalue)
            # print("-" * 40)

            # Skip if branchName is not "MH-MUM-DOM"
            if branchNamevalue != "MH-MUM-DOM-ENCS":
                print(f"{student_number} -> Skipped (Branch: {branchNamevalue})")
                continue

            writer.writerow([
                student_number, mobileNumbervalue, studentNamevalue, fatherNamevalue, motherNamevalue,
                branchNamevalue, classNamevalue, courseAmountvalue, dueAmountvalue
            ])

    browser.close()

print(f"\n✅ Data saved to: {output_file}")