#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/lte-module.h"
#include "ns3/mobility-module.h"
#include "ns3/applications-module.h"

using namespace ns3;

NS_LOG_COMPONENT(MyApp);

class MyApp : public Application
{
public:
  MyApp() {}
  virtual ~MyApp() {}

  void StartApplication() override;
  void StopApplication() override;

private:
  void ScheduleTx(void);
  void SendPacket(void);

  Ptr<Socket> m_socket;
  Address m_peer;
  EventId m_sendEvent;
  uint32_t m_packetSize;
  uint32_t m_packetsSent;
};

void
MyApp::StartApplication()
{
  m_socket = Socket::CreateSocket(GetNode(), UdpSocketFactory::GetTypeId());
  InetSocketAddress remoteAddress(InetSocketAddress(m_peer, 9));
  m_socket->Bind();
  m_socket->Connect(remoteAddress);
  SendPacket();
}

void
MyApp::StopApplication()
{
  m_socket = 0;
  NS_LOG_FUNCTION(this);
  CancelEvent(m_sendEvent);
}

void
MyApp::SendPacket()
{
  Ptr<Packet> packet = Create<Packet>(m_packetSize);
  m_socket->Send(packet);
  m_packetsSent++;

  if (m_packetsSent < 100) { // Envía 100 paquetes
    ScheduleTx();
  }
}

void
MyApp::ScheduleTx(void)
{
  if (m_socket == 0) {
    return;
  }

  Time tNext = Seconds(1.0);
  m_sendEvent = Simulator::Schedule(tNext, &MyApp::SendPacket, this);
}

int main(int argc, char *argv[])
{
  CommandLine cmd;
  cmd.Parse(argc, argv);

  // Crear nodos
  NodeContainer ueNodes, enbNodes;
  ueNodes.Create(2);
  enbNodes.Create(1);

  // Configurar movilidad
  MobilityHelper mobility;
  mobility.SetPositionAllocator("ns3::RandomDiscPositionAllocator",
                               "X", DoubleValue(0.0),
                               "Y", DoubleValue(0.0),
                               "Radius", DoubleValue(50.0));
  mobility.SetMobilityModel("ns3::RandomWaypointMobilityModel",
                           "Speed", DoubleValue(5.0),
                           "PauseTime", TimeValue(Seconds(5.0)));
  mobility.Install(ueNodes);

  // Configurar LTE, instalar dispositivos e Internet
  // ... (código similar al anterior)

  // Crear aplicaciones
  uint32_t packetSize = 1500;
  TypeId tid = TypeId::LookupByName("ns3::UdpSocketFactory");
  Ptr<SocketFactory> factory = SocketFactory::CreateSocketFactory(tid);
  InetSocketAddress remoteAddress(InetSocketAddress(enbIp, 9));

  for (uint32_t i = 0; i < ueNodes.GetN(); ++i) {
    Ptr<MyApp> client = CreateObject<MyApp>();
    client->m_packetSize = packetSize;
    client->m_peer = remoteAddress;
    ueNodes.Get(i)->AddApplication(client);
    client->SetStartTime(Seconds(1.0));
    client->SetStopTime(Seconds(10.0));
  }

  // Ejecutar simulación
  Simulator::Run();
  Simulator::Destroy();

  return 0;
}
