BEGIN;
--
-- Create model Categoria
--
CREATE TABLE "tienda_categoria" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(100) NOT NULL);
--
-- Create model Pedido
--
CREATE TABLE "tienda_pedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fecha" datetime NOT NULL, "total" integer NOT NULL, "usuario_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Perfil
--
CREATE TABLE "tienda_perfil" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "telefono" varchar(20) NULL, "direccion" varchar(255) NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Producto
--
CREATE TABLE "tienda_producto" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nombre" varchar(100) NOT NULL, "descripcion" text NOT NULL, "precio" integer NOT NULL, "stock" integer NOT NULL, "imagen" varchar(200) NOT NULL, "categoria_id" bigint NOT NULL REFERENCES "tienda_categoria" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model DetallePedido
--
CREATE TABLE "tienda_detallepedido" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer NOT NULL, "subtotal" integer NOT NULL, "pedido_id" bigint NOT NULL REFERENCES "tienda_pedido" ("id") DEFERRABLE INITIALLY DEFERRED, "producto_id" bigint NOT NULL REFERENCES "tienda_producto" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Carrito
--
CREATE TABLE "tienda_carrito" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "usuario_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "tienda_carrito_productos" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "carrito_id" bigint NOT NULL REFERENCES "tienda_carrito" ("id") DEFERRABLE INITIALLY DEFERRED, "producto_id" bigint NOT NULL REFERENCES "tienda_producto" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "tienda_pedido_usuario_id_a3683866" ON "tienda_pedido" ("usuario_id");
CREATE INDEX "tienda_producto_categoria_id_6dc179b4" ON "tienda_producto" ("categoria_id");
CREATE INDEX "tienda_detallepedido_pedido_id_b3eb1187" ON "tienda_detallepedido" ("pedido_id");
CREATE INDEX "tienda_detallepedido_producto_id_1e766595" ON "tienda_detallepedido" ("producto_id");
CREATE INDEX "tienda_carrito_usuario_id_488f5349" ON "tienda_carrito" ("usuario_id");
CREATE UNIQUE INDEX "tienda_carrito_productos_carrito_id_producto_id_f597c4a9_uniq" ON "tienda_carrito_productos" ("carrito_id", "producto_id");
CREATE INDEX "tienda_carrito_productos_carrito_id_9dee4276" ON "tienda_carrito_productos" ("carrito_id");
CREATE INDEX "tienda_carrito_productos_producto_id_44581a55" ON "tienda_carrito_productos" ("producto_id");
COMMIT;