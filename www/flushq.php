<?php
    passthru ("/usr/local/bin/avocado --flush 2>&1");
    header('Location: /');
?>
