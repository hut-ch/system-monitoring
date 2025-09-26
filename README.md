# System Monitoring

Streaming system monitoring data (CPU, memory, disk and network) to Kafka for later consumption and visualisation

This project uses ``psutils`` python library to record system metrics and send them to kafka topics for consumption. There is a grafana dashboard connecting directly to the topics displaying current metrics.

<img width="1212" height="1161" alt="sys-mon-dash" src="https://github.com/user-attachments/assets/648d909b-690c-4641-a202-939e1eda0bb2" />

``TODO:`` create kafka consumer to store and aggregate metrics over time

---

# Quickstart
1. Clone/download repository
   - either [clone the repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) or at the top of the page click the <span style="color:green">Green</span> ``Code`` button then select ``Download Zip`` to download the repository and unzip
1. Start the Container
    - Ensure docker is running (bottom left corner of docker desktop check for ``Engine running``)
    - Open a terminal/command prompt and navigate to the main folder of the repository. If on windows you may be able to ``shift + right click`` in the folder and select ``Open in Terminal`` or ``Open Powershell window here``.  
    - Inside the terminal type ``docker compose up`` and the containers should start to build and run  
    - Once started the container should now be visible in docker desktop and the terminal window can be closed
1. View Kafka UI
    - The kafka-ui container has been provided to allow visibility of the streaming messages herehttp://localhost:44082/
      <img width="1540" height="453" alt="kafka-topics" src="https://github.com/user-attachments/assets/ff883fa3-da0b-4ab1-a001-3ec77ef73656" />

1. View Dashboard
    - To view the live data dashboard go to http://localhost:44083/
    - Use the following credentials
      - username: ``admin``
      - password: ``grafanapw1``
    - From either the main home screen or dashboards select ``System Monitoring``
      <img width="1558" height="314" alt="grafana" src="https://github.com/user-attachments/assets/6a8beca5-4efc-4998-a3ea-addb119c93b9" />

