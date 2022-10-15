import asyncio

class My_server:
    def __init__(self, serv_host = '127.0.0.1', serv_port = 9999) -> None:
        self.serv_host = serv_host
        self.serv_port = serv_port
        self.counter = 0

    async def run(self):
        server = await asyncio.start_server(self.__serve_client,
                                            self.serv_host,
                                            self.serv_port)
        await server.serve_forever()

    async def __serve_client(self, reader, writer):
        cid = self.counter
        self.counter +=1
        print(f'Client #{cid} connected')
        
        request = await self.__read_request(reader)
        if request is None:
            print(f'Client #{self.cid} unexpectedly disconnected')
        else:
            response = await self.__handle_request(request)
            await self.__write_response(writer, response, cid)

    async def __read_request(self, reader):
        delimiter = b'!'
        request = bytearray()
        try:
            while True:
                chunk = await reader.read(4)
                if not chunk:
                    return None
                
                request += chunk
                if delimiter in request:
                    return request
        except ConnectionResetError:
            return None
        except:
            raise

    async def __handle_request(self, request):
        await asyncio.sleep(10)
        return request[::-1]

    async def __write_response(self, writer, response, cid):
        writer.write(response)
        await writer.drain()
        writer.close()
        print(f'Client #{cid} has been served')


if __name__ == '__main__':
    serv = My_server()
    asyncio.run(serv.run())
