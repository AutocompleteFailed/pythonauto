<?php //22/09 this works at lest enough for the moment 23/09 works from button press
// https://gist.github.com/pierrejoye/1094669   this works but still have issue with infinite lockup 22/09

$PassedVars = $_REQUEST["q"];
$VarList = explode("$", $PassedVars);
$StudentNumber = $VarList[0];
$TestName = $VarList[1];

$generate_yaml_cmd = escapeshellcmd("/var/www/html/tsugi/mod/pythonauto/util/yaml_cast.py -i {$StudentNumber} -o {$TestName}");
$generate_yaml_cmd_output = shell_exec($generate_yaml_cmd);
echo $generate_yaml_cmd_output;

//$cmd = "/var/www/html/tsugi/mod/pythonauto/qemu-arm/xpack-qemu-arm-2.8.0-9/bin/qemu-system-gnuarmeclipse";
//$cmd = "avocado --config /var/www/html/tsugi/mod/pythonauto/tests/modify_var_elf.py.data/modify_var_elf.yaml --show=test run /var/www/html/tsugi/mod/pythonauto/tests/modify_var_elf.py:PrintVariableTest.test";
$cmd = 'bash -c "avocado run /var/www/html/tsugi/mod/pythonauto/tests/modify_var_elf.py:PrintVariableTest.test"';

//$parts = array(
	//'-jar' => 'G:\\test\\yuic\\build\\yuicompressor-2.4.6.jar',
//	'--board' => 'STM32F0-Discovery',
//	'--image' => "/var/www/html/tsugi/mod/pythonauto/StudentFiles/{$StudentNumber}/{$StudentNumber}.elf",
//    '--verbose' => '--verbose', // cheeky hack to get two copies of --verbose into the args. multiple entries don't work since it just rewrites the same key repeatedly.
//	'-nographic' => '',
//	'-d' => 'unimp,guest_errors'
	//'--semihosting-config' => 'enable=on,target=native'
	//'H:\\projects\\assetic\\assetic\\tests\\Assetic\\Test\\Filter\\fixtures\\cssmin\\fonts.css -o g:\\temp\\test.css',
	//'-o' => 'g:\\temp\\test.css',
//);

/* $args = '';
foreach ($parts as $k => $part) { //single quotes on the nographic arg causes a bug which crashes the program.
	if (is_string($k)) {
		//$args .= ' ' . escapeshellarg($k) . ' ' . escapeshellarg($part);
		$args .= ' ' . $k . ' ' . $part;
	} else {
		//$args .= ' ' . escapeshellarg($part);
		$args .= ' ' . $part;
	}
} */

//$process_cmd = '"' . $cmd . '"' . ' ' . $args;
//$process_cmd = "timeout -k 10 5 ". $cmd . ' ' . $args;
//$process_cmd = "timeout -k 20 10 ". $cmd;
$process_cmd = $cmd;
//$process_cmd = "timeout -k 10 5 ". $cmd . ' ' . "--verbose"  . ' ' . $args; // only one instance of --verbose appears from the loop above. Prob because it just rewrites the key value pair.
//$process_cmd = $cmd  . ' ' . $args;
$errorlog = "/var/www/html/tsugi/mod/pythonauto/StudentFiles/{$StudentNumber}/{$StudentNumber}error-output.txt";
$env = NULL;
$options = array('bypass_shell' => true); // only applicable to windows
$cwd = NULL;
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("file", "$errorlog" , "a")  // stderr is a file to write to
);

$process = proc_open($process_cmd, $descriptorspec, $pipes, $cwd, $env, $options);
echo ($process_cmd);
if (is_resource($process)) {
	echo stream_get_contents($pipes[1]);
	fclose($pipes[1]);

	// It is important that you close any pipes before calling
	// proc_close in order to avoid a deadlock
	$return_value = proc_close($process);

	echo "\ncommand returned $return_value\n";
}

?>
