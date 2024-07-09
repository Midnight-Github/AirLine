from reader.Toml import Toml

#user_manager.data[<head>][<key>]
user_manager = Toml("\\..\\users\\user.toml")

#admin_manager.data[<head>][<key>]
admin_manager = Toml("\\..\\users\\admin.toml")