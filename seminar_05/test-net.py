from mock import Mock, DiskIO
import mock

class TestTelnetInterface(mock.TestCase):
    def setUp(self):
        self.setupModules(["socket"])

        self.fs = DiskIO()
        self.fs["/socket"] = ""
        self.client_file = self.fs.open("/socket", "rw")

        self.client_socket = Mock()
        self.client_socket.makefile = Mock(return_value = self.client_file)

        self.server_socket = Mock()
        self.server_socket.bind = Mock()
        self.server_socket.listen = Mock()
        self.server_socket.accept = Mock(return_value = (self.client_socket, ('127.0.0.1', 8000)))
        self.server_socket.settimeout = Mock()
        
        import socket
        socket.socket = Mock(return_value = self.server_socket)
        socket.getaddrinfo = Mock(return_value=[
            (2, 1, 6, '', ('127.0.0.1', 8000)),
            (2, 2, 17, '', ('127.0.0.1', 8000)),
            (2, 3, 0, '', ('127.0.0.1', 8000)),
            (2, 2, 17, '', ('127.0.0.2', 8000))
            ])
        socket.SOCK_STREAM = 1
        socket.SOCK_DGRAM = 2
        socket.AF_INET = 2
        socket.AF_INET6 = 10

    def tearDown(self):
        self.tearDownModules()

    def test_class(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.assertIsInstance(self.intf, interface.IRCBotTelnetInterface)

    def test_addrinfo(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf.open()

        import socket
        socket.getaddrinfo.assert_called_once_with("localhost", 8000)

    def test_no_valid_family(self):
        import socket
        socket.getaddrinfo = Mock(return_value=[
            (3, 1, 6, '', ('127.0.0.1', 8000)),
            (3, 2, 17, '', ('127.0.0.1', 8000)),
            (3, 3, 0, '', ('127.0.0.1', 8000))
            ])

        import interface
        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)

        self.assertRaises(Exception, self.intf.open, [])

    def test_no_valid_type(self):
        import socket
        socket.getaddrinfo = Mock(return_value=[
            (2, 0, 6, '', ('127.0.0.1', 8000)),
            (10, 3, 17, '', ('127.0.0.1', 8000)),
            (2, 3, 0, '', ('127.0.0.1', 8000))
            ])

        import interface
        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)

        self.assertRaises(Exception, self.intf.open, [])


    def test_socket(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf.open()

        import socket
        socket.socket.assert_called_once_with(2, 1, 6)

    def test_bind(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf.open()
        self.server_socket.bind.assert_called_once_with(('127.0.0.1', 8000))
        
    def test_listen(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf.open()
        self.server_socket.listen.assert_called()

    def test_listen_saved(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf.open()

        self.assertEquals(self.intf._listen, self.server_socket)

    def test_existing_client(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf._client = "client"
        self.assertEquals(self.intf.client(), "client")

    def test_existing_client(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf._socket = self.client_socket
        self.intf._sfile = self.client_file
        self.intf._listen = self.server_socket
        self.assertEquals(self.intf.client(), self.client_file)
    
    def test_new_client(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf._listen = self.server_socket
        self.intf._socket = None
        self.intf._sfile = None
        self.assertEquals(self.intf.client(), self.client_file)

    def test_disconnect(self):
        import interface

        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf._socket = self.client_socket
        self.intf._sfile = self.client_file
        self.intf._listen = self.server_socket
        self.intf.disconnected()
        self.assertEquals(self.intf._sfile, None)
        self.assertEquals(self.intf._socket, None)
    
    def test_read_error(self):
        class OKException(Exception):
            pass
        
        def f():
            raise OKException
        
        import interface
        self.server_socket.accept.side_effect = f

        self.fs["/socket"] = ""
        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf._socket = self.client_socket
        self.intf._sfile = self.client_file
        self.intf._listen = self.server_socket

        self.assertRaises(OKException, self.intf.read)
        
    def test_read_exception(self):
        class OKException(Exception):
            pass
        
        def f():
            raise OKException

        def r(len = 1):
            raise socket.error()
        
        import interface
        self.server_socket.accept.side_effect = f
        self.client_file.read = Mock(side_effect = r)

        self.fs["/socket"] = ""
        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.intf._socket = self.client_socket
        self.intf._sfile = self.client_file
        self.intf._listen = self.server_socket

        self.assertRaises(OKException, self.intf.read)

    def test_read(self):
        import interface

        self.fs["/socket"] = "line\nline2"
        self.intf = interface.IRCBotTelnetInterface("localhost", 8000)
        self.client_file = self.fs.open("/socket", "rw")
        self.intf._socket = self.client_socket
        self.intf._sfile = self.client_file
        self.intf._listen = self.server_socket

        self.assertEquals("line", self.intf.read())

if __name__ == "__main__":
    mock.main()
