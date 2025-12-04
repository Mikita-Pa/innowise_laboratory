DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

-- Создаем таблицу студентов
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    full_name TEXT,
    birth_year INTEGER
);

-- Создаем таблицу оценок
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject TEXT,
    grade INTEGER,
    FOREIGN KEY(student_id) REFERENCES students(id)
);


-- Вставка студентов
INSERT INTO students (full_name, birth_year) VALUES 
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

-- Вставка оценок (student_id, subject, grade)
INSERT INTO grades (student_id, subject, grade) VALUES 
(1, 'Math', 88), (1, 'English', 92), (1, 'Science', 85),
(2, 'Math', 75), (2, 'History', 83), (2, 'English', 79),
(3, 'Science', 95), (3, 'Math', 91), (3, 'Art', 89),
(4, 'Math', 84), (4, 'Science', 88), (4, 'Physical Education', 93),
(5, 'English', 90), (5, 'History', 85), (5, 'Math', 88),
(6, 'Science', 72), (6, 'Math', 78), (6, 'English', 81),
(7, 'Art', 94), (7, 'Science', 87), (7, 'Math', 90),
(8, 'History', 77), (8, 'Math', 83), (8, 'Science', 80),
(9, 'English', 96), (9, 'Math', 89), (9, 'Art', 92);

SELECT * FROM grades 
WHERE student_id = (SELECT id FROM students WHERE full_name = 'Alice Johnson');

SELECT student_id, AVG(grade) as average_grade 
FROM grades 
GROUP BY student_id;

SELECT * FROM students 
WHERE birth_year > 2004;

SELECT subject, AVG(grade) as subject_avg 
FROM grades 
GROUP BY subject;

SELECT s.full_name, AVG(g.grade) as average_grade
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average_grade DESC
LIMIT 3;

SELECT DISTINCT s.full_name
FROM students s
JOIN grades g ON s.id = g.student_id
WHERE g.grade < 80;