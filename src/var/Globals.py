from reader.Toml import Toml

#<var>.data[<head>][<key>]
user_manager = Toml("\\..\\config\\user.toml")
admin_manager = Toml("\\..\\config\\admin.toml")
database_manager = Toml("\\..\\config\\database.toml")