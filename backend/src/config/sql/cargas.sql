BEGIN TRANSACTION;
CREATE TABLE career_subject (
    career_subject_id SERIAL PRIMARY KEY,
    career_id INT NOT NULL,
    subject_id INT NOT NULL,
    FOREIGN KEY (career_id) REFERENCES career(career_id),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_id)
);
INSERT INTO career(career_name) VALUES ('Ingeniería en Sistemas');
INSERT INTO career(career_name) VALUES ('Ingeniería en Electrónica');
INSERT INTO career(career_name) VALUES ('Ingeniería en Mecanica');  
INSERT INTO career(career_name) VALUES ('Psicología');
INSERT INTO career(career_name) VALUES ('Derecho');
INSERT INTO career(career_name) VALUES ('Medicina');

INSERT INTO subject(subject_name) VALUES ('Matemáticas');
INSERT INTO subject(subject_name) VALUES ('Física');
INSERT INTO subject(subject_name) VALUES ('Química');
INSERT INTO subject(subject_name) VALUES ('Biología');
INSERT INTO subject(subject_name) VALUES ('Historia');
INSERT INTO subject(subject_name) VALUES ('Geografía');
INSERT INTO subject(subject_name) VALUES ('Filosofía');
INSERT INTO subject(subject_name) VALUES ('Inglés');
INSERT INTO subject(subject_name) VALUES ('Francés');
INSERT INTO subject(subject_name) VALUES ('Alemán');
INSERT INTO subject(subject_name) VALUES ('Italiano');
INSERT INTO subject(subject_name) VALUES ('Portugués');
INSERT INTO subject(subject_name) VALUES ('Programación');
INSERT INTO subject(subject_name) VALUES ('Base de Datos');
INSERT INTO subject(subject_name) VALUES ('Redes');
INSERT INTO subject(subject_name) VALUES ('Sistemas Operativos');
INSERT INTO subject(subject_name) VALUES ('Diseño');
INSERT INTO subject(subject_name) VALUES ('Cálculo');
INSERT INTO subject(subject_name) VALUES ('Álgebra');
INSERT INTO subject(subject_name) VALUES ('Estadística');
INSERT INTO subject(subject_name) VALUES ('Probabilidad');
INSERT INTO subject(subject_name) VALUES ('Mecánica');
INSERT INTO subject(subject_name) VALUES ('Termodinámica');
INSERT INTO subject(subject_name) VALUES ('Electromagnetismo');
INSERT INTO subject(subject_name) VALUES ('Circuitos');
INSERT INTO subject(subject_name) VALUES ('Electrónica');
INSERT INTO subject(subject_name) VALUES ('Control');
INSERT INTO subject(subject_name) VALUES ('Automatización');
INSERT INTO subject(subject_name) VALUES ('Psicología General');
INSERT INTO subject(subject_name) VALUES ('Psicología Social');

INSERT INTO career_subject(career_id, subject_id) VALUES (1, 13);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 14);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 15);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 16);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 17);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 18);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 19);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 20);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 21);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 23);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 24);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 27);
INSERT INTO career_subject(career_id, subject_id) VALUES (1, 28);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 13);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 14);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 15);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 16);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 17);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 18);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 19);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 20);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 21);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 23);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 24);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 25);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 26);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 27);
INSERT INTO career_subject(career_id, subject_id) VALUES (2, 28);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 17);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 18);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 19);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 20);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 21);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 22);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 23);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 24);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 27);
INSERT INTO career_subject(career_id, subject_id) VALUES (3, 28);
INSERT INTO career_subject(career_id, subject_id) VALUES (4, 7);
INSERT INTO career_subject(career_id, subject_id) VALUES (4, 29);
INSERT INTO career_subject(career_id, subject_id) VALUES (4, 30);
INSERT INTO career_subject(career_id, subject_id) VALUES (5, 7);
INSERT INTO career_subject(career_id, subject_id) VALUES (5, 29);
INSERT INTO career_subject(career_id, subject_id) VALUES (5, 30);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 1);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 2);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 3);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 4);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 5);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 6);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 8);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 9);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 10);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 11);
INSERT INTO career_subject(career_id, subject_id) VALUES (6, 12);
COMMIT TRANSACTION;


