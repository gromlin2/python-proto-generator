from python_proto_generator.proto_python import hello_world_pb2

helloPlanet = hello_world_pb2.HelloPlanet()
helloPlanet.message = "aAGxrLXuGe"
helloPlanet.planet = "rpsdewRFau"
helloPlanet.be_friendly = True

print(helloPlanet)

debtsAtPlanet = hello_world_pb2.DebtsAtPlanet()
debtsAtPlanet.amount_of_cash_carried = 3586303089
debtsAtPlanet.amount_of_debt = 1222670901

print(debtsAtPlanet)