import cmd, ssl, os
from suds.client import Client

# Ignore SSL errors. Remove this when launching nukes
ssl._create_default_https_context = ssl._create_unverified_context

class WSO2Server(cmd.Cmd):
    """Command line processor"""
    prompt = "(WSO2) > "
    cookie = None   # hold the cookie after calling AuthenticatinoAdmin, for subsequent calls
    host = None     # hostname:port combo
    client = None   # suds Client object
    methods = []    # hold operations under an admin service, used for autocompletion

    def do_connect(self, line):
        """
connect hostname:port username password
        """
        args = line.split(" ")

        if len(args) == 3:
            authClient = Client('file://' + os.getcwd() + '/as/5.2.1/AuthenticationAdmin.wsdl', 
                location="https://{0}/services/AuthenticationAdmin".format(args[0]))
            hostname = args[0].split(":")[0]
            status = authClient.service.login(args[1], args[2], hostname)
            if status == True:
                version = Client('https://{}/services/Version?wsdl'.format(args[0]),
                    location='https://{0}/services/Version'.format(args[0]))
                serverType = version.service.getVersion()

                # setting cookiejar for subsequent admin service calls
                self.cookie = authClient.options.transport.cookiejar

                # need the host for subsequent admin calls
                self.host = args[0]

                print("Connected to " + serverType)
                self.prompt = "(WSO2 - " + serverType + ") > "

    def isAuthenticated(self):
        if self.cookie is None:
            print("Not connected to a server. Type help connect")
            return False
        else:
            return True

    def do_call(self, line):
        """
call AdminServiceName.operation(value1, value2)

Type call AdminServiceName.<TAB><TAB> to see operations
        """
        if self.isAuthenticated():
            sIndex = line.find(".")
            adminService = line[:sIndex]
            serviceCall = line[sIndex+1:]

            client = Client('https://{0}/services/{1}?wsdl'.format(self.host, adminService),
                location='https://{0}/services/{1}'.format(self.host, adminService))
            client.options.transport.cookiejar = self.cookie
            print(eval("client.service.{0}".format(serviceCall)))

    def complete_call(self, text, line, begidx, endidx):
        if text.endswith("."):
            # show all methods under the admin service
            self.client = Client('https://{0}/services/{1}?wsdl'.format(self.host, text[:len(text)-1]),
                location='https://{0}/services/{1}'.format(self.host, text[:len(text)-1]))
            output = str(self.client)
            # create an array of methods from the serialized client string
            self.methods = [ x.strip() for x in output[ output.find("Method") : output.find("Types")-1 ].split("\n")[1:] ]
            return self.methods
        elif len(text)-2 >= text.find("."):
            # starting to type a name of a method
            startText = text[text.find(".")+1:]
            serviceName = text[:text.find(".")+1]
            completions = [ serviceName+m for m in self.methods if m.startswith(startText)]
            if len(completions) == 1:
                # return empty method without params
                name = completions[0]
                return [ name[:name.find("(")] + "()" ]
            else:
                return completions
        else:
            return self.methods

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    try:
        WSO2Server().cmdloop()
    except KeyboardInterrupt as e:
        exit()