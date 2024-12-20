The file contains ICMP PIng

Ping is a tool used to measure delay and loss in computer networks. It
does this by sending messages to another host. Once a message has reached that host, it is
sent back to the sender. By measuring the amount of time taken to receive that response, we
can determine the delay in the network. Similarly, by tracking the responses returned from
our messages, we can determine if any have been lost in the network.

Trace Route

This is used to measure
latency between the host and each hop along the route to a destination. This too uses an
ICMP echo request message, but with an important modification: the Time To Live (TTL)
value is initially set to 1. This ensures that we get a response from the first hop; the network
device closest to the host we are running the script on. When the message arrives at this
device, the TTL counter is decremented. When it reaches 0 (in this case at the first hop), the
message is returned to the client with an ICMP type of 11. This indicates that TTL has been
exceeded. As with the previous task, by measuring the time taken to receive this response,
delay can be calculated at each hop in the network. This process can be repeated, increasing
the TTL each time, until we receive an echo reply back (with an ICMP type of 0). This tells
us that we have reached the destination, so we can stop the script.

Paris Traceroute

Well-known limitation of trace route is that it may indicate a path that does not actually
exist in the presence of “load-balancers” in the network.Paris-traceroute is a modified traceroute that does not modify the flow identifiers of
subsequent packets (unlike traceroute), and therefore a paris-traceroute traffic between the
same source and destination should follow the same path even in the presence of flow-based
splitting of traffic by the load-balancers.

Web Server

We will be using network sockets to build our application and to
interact with the network. The Web Server differs from the ICMP Ping application in that it
will bind to an explicit socket, identified by a port number. This allows the Web Server to
listen constantly for incoming requests, responding to each in turn. HTTP traffic is usually
bound for port 80, with port 8080 a frequently used alternative

Web Proxy

However, when we use a Web Proxy, we place this additional application between the
client and the web server. Now, both the request message sent by the client, and the
response message delivered by the web server, pass through the Web Proxy. In other
words, the client requests the objects via the Web Proxy. The Web Proxy will forward the
client’s request to the web server. The web server will then generate a response message
and deliver it to the proxy server, which in turn sends it to the client.

