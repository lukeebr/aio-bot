@echo off

set "{{=setlocal enableDelayedExpansion&for %%a in (" & set "}}="::end::" ) do if "%%~a" neq "::end::" (set command=!command! %%a) else (call !command! & endlocal)"

%{{%
    pyarmor pack
    -x " --advanced 2 --bootstrap 2 --enable-suffix --exclude helheim"
    -e "
        --add-data 'C:\Users\lukeb\Desktop\aio0.2\helheim/^;helheim'
        --add-binary 'C:\Users\lukeb\Desktop\aio0.2\helheim/pytransform_vax_000061.pyd^;helheim'
        --add-data 'C:\Users\lukeb\AppData\Local\Programs\Python\Python38\Lib\site-packages\cloudscraper^;cloudscraper'
	--add-data 'C:\Users\lukeb\AppData\Local\Programs\Python\Python38\Lib\site-packages\pyfiglet^;pyfiglet'
        -c
        --onefile
        --hidden-import dateutil.parser
        --hidden-import helheim
        --hidden-import cloudscraper
        --hidden-import cryptography
        --hidden-import polling2
        --hidden-import PIL
        --hidden-import PIL.Image
    "
    --name ExoCLI
    main.py
%}}%
