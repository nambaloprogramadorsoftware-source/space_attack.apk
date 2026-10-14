[app]
title = Ebenesis gamer
package.name = ebenesisgamer
package.domain = com.exemplo
source.dir = .
source.include_exts = py,png,mp3,txt
version = 1.0.0
requirements = python3,kivy

# Configuração do Ícone Oficial
android.presplash_color = #01021A
icon.filename = %(source.dir)s/jogador.png

# Configurações Universais para Android
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
