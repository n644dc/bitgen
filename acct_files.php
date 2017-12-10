<?php
$path    = 'bitcon';
$output = array();
foreach( new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator( $path, FilesystemIterator::SKIP_DOTS | FilesystemIterator::UNIX_PATHS ) ) as $value ) {
        if ( $value->isFile() ) {
            $output[] = array( $value->getMTime(), $value->getPathname() );
        }
}

usort ( $output, function( $a, $b ) {
    return $a[0] > $b[0];
});

foreach ($output as $a) {
	echo '<a href=\'http://'.$_SERVER['HTTP_HOST'].'/'.$a[1].'\'>'.$a[1].'</a><br />';
}
?>