<?php
    passthru ("/usr/local/bin/avocado --flush-cache 2>&1");
    header('Location: /');
?>
