import os
import shutil
import time
import logging
#from gdb_interface import GDBInterface

from avocado import Test
from avocado.utils import build, gdb, process



class PrintVariableTest(Test):

    """
    This demonstrates the GDB API
    1) it executes C program which prints MY VARIABLE 'A' IS: 0
    2) using GDB it modifies the variable to ff
    3) checks the output
    :avocado: tags=requires_c_compiler
    :param source: name of the source file located in a data directory
    """

    __binary = None   # filename of the compiled program


    def setUp(self):
        """
        Build 'print_variable'.
        """
        #Test(base_logdir="/var/www/html/tsugi/mod/pythonauto/StudentFiles/Results")
        #source = self.params.get('source', default="/var/www/html/tsugi/mod/pythonauto/stm32f0-discovery-basic-template/src/main.c") #this is beyond janky
        """ source = self.params.get('source', default="/var/www/html/tsugi/mod/pythonauto/testproj/src/main.c") #this is beyond janky
        
        c_file = self.get_data(source)
        if c_file is None:
            self.cancel('Test is missing data file %s' % source)
        #shutil.copy(c_file, self.workdir)
        try:
            shutil.copy(c_file, "/var/www/html/tsugi/mod/pythonauto/testproj/src")
        except:
            print("SameFileError probably")
        
        self.__binary = c_file
        
        self.__binary = source.rsplit('.', 1)[0]
        build.make(self.workdir,
                   env={'CFLAGS': '-g3 -O0'},
                   extra_args=self.__binary)
        self.__binary = source.rsplit('.', 1)[0] + '.elf'
        build.make("/var/www/html/tsugi/mod/pythonauto/testproj/Debug",
                   extra_args='clean')
        build.make("/var/www/html/tsugi/mod/pythonauto/testproj/Debug",
                   extra_args='testproj.elf')
        logger = logging.getLogger()
        logfile_handler = logging.FileHandler(filename = "/tmp/job_{p}_time_{t}.log".format(
            p = Test.job, t = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())))
        logger.setLevel(logging.DEBUG)
        logfile_handler.setLevel(level=logging.DEBUG)
        logfile_handler.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT))
        logger.addHandler(logfile_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(asctime)s:" + logging.BASIC_FORMAT))
        logger.addHandler(console_handler) """

    def test(self):
        """
        Execute 'print_variable'.
        """
        qemu_exe_path = "/home/automark/Work/qemu-arm-dev/linux-x64/install/qemu-arm/bin/qemu-system-gnuarmeclipse"
        #image_path = "/var/www/html/tsugi/mod/pythonauto/stm32f0-discovery-basic-template/main.elf"
        image_path = "/var/www/html/tsugi/mod/pythonauto/testproj/Debug/testproj.elf"
        qemu_invoke_string = qemu_exe_path + " -s -S --board UCT-Development --image %s --verbose --nographic --verbose -d unimp,guest_errors"%image_path # -realtime wants a parameter but I cna't find any valid ones
        #qemu = process.SubProcess("/var/www/html/tsugi/mod/pythonauto/qemu-arm/xpack-qemu-arm-2.8.0-9/bin/qemu-system-gnuarmeclipse -s -S --board STM32F0-Discovery --verbose --nographic --verbose -d unimp,guest_errors", shell=False)
        qemu = process.SubProcess(qemu_invoke_string, shell=False)
        qemu.start()
        
        app = gdb.GDB(path='/usr/bin/gdb-multiarch', exec_path=image_path)
        app.set_file(image_path)
        app.connect('1234')
        #app.load()     # to avoid error about peripheral not being initialized I'm starting the server with a target image which seems to make it functional. Error still displays though
        app.cmd("b main")
        app.cmd("info break")       # GPIOA 0x4800 0000 - 0x4800 03FF
        app.cmd("display/th 0x48000414") # GPIOB ODR
        app.cmd("display/th 0x48000010") # GPIOA IDR
        app.cmd("display/d TIM14_IRQHandler::t")

        app.set_watch('*0x48000414')
        app.continue_()
        app.read_until_break()      # here gdb will stop when ODR written to or another breakpoint occurs
        GPIOB = app.read_from_address(0x48000414)
        #app.continue_()
        #app.read_until_break()
        GPIOB = app.read_from_address(0x48000414)
        #app.continue_()
        #app.read_until_break()
        GPIOB = app.read_from_address(0x48000414)
        app.disconnect()
        print("Qemu about to stop",end='')
        qemu.stop()
        #out_reg = GPIOC.stream_messages[0].__dict__     # this works, may be useful
        #self.assertIn("MY VARIABLE 'A' IS: 200", str(GPIOB.stream_messages))
        self.assertIn("0x48000414:\\t0x00000000", str(GPIOB.stream_messages[0].__dict__))