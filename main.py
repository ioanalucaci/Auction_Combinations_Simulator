from auction import *
import metrics_writer as mw
import parameters_reader as pr
import time

# TODO: Work on connecting the .txt file with the main file
# GNU plot(?) and vectorised plots

list_of_auctions = []
start = time.time()

number_of_rounds, parameters, bidders = pr.read_parameters()

for x in range(0, number_of_rounds):
    model = Auction(parameters, bidders)
    model.step()
    list_of_auctions.append(model)
    # print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
end = time.time()

print("I am done with the models! It took {0}".format(end - start))

mw.write_metrics(list_of_auctions)

print("Writing took {0}".format(time.time() - end))
