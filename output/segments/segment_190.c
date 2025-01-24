void main() {
 int csd, len;
 char sendmsg[30], recvmsg[20];
 struct sockaddr_in cliaddr, servaddr;
 csd = socket(
             2
                    , 
                      SOCK_STREAM
                                 , 0);
 servaddr.sin_family = 
                      2
                             ;
 servaddr.sin_port = htons(33345);
 servaddr.sin_addr.s_addr = htonl(
                                 ((in_addr_t) 0x00000000)
                                           );
 connect(csd, (struct sockaddr*)&servaddr, sizeof(servaddr));
 while(1) {
  printf("Client: ");
  fgets(sendmsg, 30, 
                    stdin
                         );
  len = strlen(sendmsg);
  sendmsg[len-1] = '\0';
  send(csd, sendmsg, 20, 0);
  recv(csd, recvmsg, 20, 0);
  printf("Server: %s\n", recvmsg);
 }
 int x = close(csd);
 return 0;
}
