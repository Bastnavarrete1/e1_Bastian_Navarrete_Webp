-- USUARIOS

INSERT INTO auth_user (id, username, password, email, is_superuser, is_staff, is_active)
VALUES (1, 'Prueba2', 'pbkdf2_sha256$1200000$UwNvlcx8oa8BnGj1reiNv9$', 'Duoc@duoc.cl', 1, 1, 1);

INSERT INTO auth_user (id, username, password, email, is_superuser, is_staff, is_active)
VALUES (5, 'Bastian', 'pbkdf2_sha256$1200000$8OQ44xlKkxuen8xEGITQtO$', '', 0, 0, 1);

INSERT INTO auth_user (id, username, password, email, is_superuser, is_staff, is_active)
VALUES (6, 'Examen', 'pbkdf2_sha256$1200000$n9Pe8vZV5WY2fEiojw5dhY$', 'Duoc1@duoc.cl', 0, 0, 1);

INSERT INTO auth_user (id, username, password, email, is_superuser, is_staff, is_active)
VALUES (7, 'Examen3', 'pbkdf2_sha256$1200000$15LfagMKwNiG6sfCNElnw5$', 'duoc2@duoc.cl', 0, 0, 1);

-- CATEGORIAS

INSERT INTO tienda_categoria (id, nombre) VALUES (1, 'Liquidos');
INSERT INTO tienda_categoria (id, nombre) VALUES (2, 'Accesorios');
INSERT INTO tienda_categoria (id, nombre) VALUES (3, 'Atomizadores');

-- PRODUCTOS

INSERT INTO tienda_producto (id, nombre, descripcion, precio, stock, imagen, categoria_id)
VALUES (1, 'Liquido sabor Frambuesa', 'Rico liquido sabor frambuesa con hielo', 19990, 10, 'https://dojiw2m9tvv09.cloudfront.net/39213/product/trap-queen6872.png', 1);

INSERT INTO tienda_producto (id, nombre, descripcion, precio, stock, imagen, categoria_id)
VALUES (2, 'Liquido sabor Melon', 'Sabor melon mentolado', 18990, 20, 'https://dojiw2m9tvv09.cloudfront.net/39213/product/bombo-bar-juice-ultra-melon-120ml-3mg-cl-with-ingredients6407.png', 1);

INSERT INTO tienda_producto (id, nombre, descripcion, precio, stock, imagen, categoria_id)
VALUES (3, 'Algodon Premium', 'Algodon de alta calidad para atomizadores', 5000, 30, 'https://dojiw2m9tvv09.cloudfront.net/39213/product/cotton-bacon-prime-pic-1024x1024-1049b530.jpg', 2);