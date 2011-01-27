from RapidRacer_defines import get_rs_file_info#, link_finder
if __name__ == "__main__":
	file1 = get_rs_file_info.RSFile("http://rapidshare.com/files/120453782/2002")
	print file1.get_status()
	file1.reset_url("http://rapidshare.com/files/305232527/BatyasSeele.part1.rar.html")
	print file1.get_status()
	print "Hallo Welt"