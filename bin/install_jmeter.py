import os, urllib2, zipfile, distutils.core

jmeter_version = "2.10"
jmeter_dir = "apache-jmeter-%s/" % jmeter_version
download_dir = "tmp/"

if not os.path.exists(download_dir):
    os.makedirs(download_dir)


def get_file(url, local_path):
    print("Downloading " + url)
    stream = urllib2.urlopen(url)
    with(open(download_dir + local_path, "wb")) as f:
        f.write(stream.read())

def unzip_plugin(zip_file, to_dir):
    out = jmeter_dir + to_dir
    with(zipfile.ZipFile(download_dir + zip_file, "r")) as z:
        z.extractall(out)
        distutils.dir_util.copy_tree(out + "/lib", jmeter_dir + "/lib")
        distutils.dir_util.remove_tree(out + "/lib")
    print("JMeter Plugin copied to JMeter lib directory. README for the plugin available at %s%s" % (jmeter_dir, to_dir))

def install_jmeter():
    if not os.path.exists(jmeter_dir):
        print("Download JMeter")

        jmeter_file = "http://apache.mirrors.tds.net/jmeter/binaries/apache-jmeter-%s.zip" % jmeter_version
        get_file(jmeter_file, "jmeter.zip")

        with(zipfile.ZipFile(download_dir + "jmeter.zip", "r")) as z:
            z.extractall()

        os.chmod(jmeter_dir + "/bin/jmeter.sh", 0755)
    else:
        print("JMeter directory [%s] exists... skipping" % jmeter_dir)

def install_plugins():

    if not os.path.exists(jmeter_dir + "lib/ext/JMeterPlugins-Standard.jar"):
        print("Installing JMeter Plugins")

        get_file("http://jmeter-plugins.org/downloads/file/JMeterPlugins-Standard-1.1.2.zip", "jmp-standard.zip")
        get_file("http://jmeter-plugins.org/downloads/file/JMeterPlugins-Extras-1.1.2.zip", "jmp-extras.zip")
        get_file("http://jmeter-plugins.org/downloads/file/JMeterPlugins-ExtrasLibs-1.1.2.zip", "jmp-extraslibs.zip")

        unzip_plugin("jmp-standard.zip", "jmp-standard")
        unzip_plugin("jmp-extras.zip", "jmp-extras")
        unzip_plugin("jmp-extraslibs.zip", "jmp-extraslibs")
    else:
        print("JMeter plugins appear to exist in %slib/ext" % jmeter_dir)



if __name__ == '__main__':
    install_jmeter()
    install_plugins()
    distutils.dir_util.remove_tree(download_dir)