<?php
    passthru ("/usr/local/bin/avocado --flush-kiosk 2>&1");
    header('Location: /');
?>
