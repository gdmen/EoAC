<?php
if(!empty($_REQUEST["id"]) && !empty($_REQUEST["key"])){
   
  foreach(array_keys($_REQUEST) as $var){
      $$var = $_REQUEST[$var];
  }
	$autoexec_cfg =
"bind \"F12\" jscreenshot;
alias start_intermission [
  jscreenshot;
]
alias jscreenshot [
  screenshot;
  jerboa_screenshot_info;
]
// [JERBOA] DO NOT ALTER OR DELETE THIS COMMENT: $id $key
alias jerboa_screenshot_info [
  minutesremaining;
  server_info = (concatword \"[jerboa]server_info \" (curmap 1));
  server_info = (concatword \$server_info (concatword \" \" (curmode)));
  server_info = (concatword \$server_info (concatword \" \" (curmastermode)));
  server_info = (concatword \$server_info (concatword \" \" (curserver)));
  echo \$server_info;
  loop i 25 [
    if (! (strcmp (at (pstat_score \$i) 5) \"\")) [
      pstat_info = (concatword \"[jerboa]pstat_info \" (concatword \$i (concatword \" \" (pstat_score \$i))));
      pstat_info = (concatword \$pstat_info (concatword \" \" (pstat_weap \$i)));
      echo \$pstat_info;
    ]
  ]
  echo \"[jerboa]complete\";
  loop i 6 [
    echo \"\";
  ]
]";
	header("Cache-Control: public");
	header("Content-Description: File Transfer");
	header("Content-Length: ". strlen($autoexec_cfg) .";");
	header("Content-Disposition: attachment; filename=autoexec.cfg");
	header("Content-Type: text/plain; ");
	header("Pragma: no-cache");
	header("Content-Transfer-Encoding: binary");
	
	echo $autoexec_cfg;
}
?>