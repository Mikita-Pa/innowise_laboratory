def main():
    # 1. Данные студентов (Начальная точка)
    # Создаем пустой список для хранения словарей студентов
    students = []

    # 2. Основной цикл программы (Меню)
    while True:
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report (all students)")
        print("4. Find top student")
        print("5. Exit")

        # Обработка ввода пункта меню
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            name = input("Enter student name: ")
            
            # Проверка, существует ли студент
            student_exists = False
            for student in students:
                if student['name'] == name:
                    print(f"Student '{name}' already exists.")
                    student_exists = True
                    break
            
            # Если не существует, создаем новый словарь
            if not student_exists:
                new_student = {"name": name, "grades": []}
                students.append(new_student)
                # (В скриншотах явного сообщения об успехе нет, но логически оно здесь)
        
        elif choice == 2:
            name = input("Enter student name: ")
            found_student = None
            
            # Поиск студента в списке
            for student in students:
                if student['name'] == name:
                    found_student = student
                    break
            
            if found_student:
                while True:
                    grade_input = input("Enter a grade (or 'done' to finish): ")
                    
                    if grade_input.lower() == 'done':
                        break
                    
                    # Обработка ошибок ввода оценки
                    try:
                        grade = int(grade_input)
                        if 0 <= grade <= 100:
                            found_student['grades'].append(grade)
                        else:
                            print("Grade must be between 0 and 100.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                print(f"Student '{name}' not found.")

        elif choice == 3:
            print("--- Student Report ---")
            if not students:
                print("No students to show.")
                continue

            all_averages = []

            for student in students:
                # Использование try/except для обработки деления на ноль (ZeroDivisionError)
                try:
                    avg = sum(student['grades']) / len(student['grades'])
                    print(f"{student['name']}'s average grade is {avg:.1f}.")
                    all_averages.append(avg)
                except ZeroDivisionError:
                    print(f"{student['name']}'s average grade is N/A.")
            
            print("-" * 30)
            
            # Вывод общей статистики, если есть хотя бы одна средняя оценка
            if all_averages:
                max_avg = max(all_averages)
                min_avg = min(all_averages)
                overall_avg = sum(all_averages) / len(all_averages)
                
                print(f"Max Average: {max_avg:.1f}")
                print(f"Min Average: {min_avg:.1f}")
                print(f"Overall Average: {overall_avg:.1f}")
            else:
                print("Not enough data for summary stats.")

        # --- Option 4: Find top performer ---
        elif choice == 4:
            # Сначала фильтруем студентов, у которых есть оценки, чтобы избежать ошибок
            students_with_grades = [s for s in students if len(s['grades']) > 0]
            
            if not students_with_grades:
                print("No students with grades found.")
            else:
                # Использование max() с lambda-функцией в качестве ключа (как в задании)
                top_student = max(
                    students_with_grades, 
                    key=lambda s: sum(s['grades']) / len(s['grades'])
                )
                
                top_avg = sum(top_student['grades']) / len(top_student['grades'])
                print(f"The student with the highest average is {top_student['name']} with a grade of {top_avg:.1f}.")

        elif choice == 5:
            print("Exiting program.")
            break
        
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()