# eaCICD
### Description
One of most easy use auto deploy system  
### How to use
1. Clone repo
2. Edit config file in cloned repo
3. Open terminal in cloned repo
4. Type `source /venv/bin/activate`
5. Type `python main.py`
6. Go to your git repository > settings > webhooks
7. Create new webhook (push only) with address <your_public_ip:your_port>/new-commit
8. Save

After first start eaCICD will create an eaCICD directory in repository folders typed in configs  
eaCICD directory contains deploy.sh and deploy.bat files for Linux and Windows systems.  
You can change this files as you wish.  
If you need to reset files to default just delete eaCICD folder and restart eaCICD

### Config file rules
#### Config example
```
{
  "host": "192.168.0.5",
  "port": 8000,
  "OSType": "W",
  "repositories": [
    {
      "name": "testRepo",
      "location": "C:\\Users\\User\\Documents\\Projects\\testRepo"
    },
    {
      "name": "testRepo1",
      "location": "C:\\Users\\User\\Documents\\Projects\\testRepo1"
    }
  ]
}
```
#### General settings
host: Your local ip address
port: port for eaCICD server
OSType: Type of operation system (L - linux, W - windows)  
repositories: List of your repositories
#### Repository settings
name: name of your repository (like in git)  
location: location of cloned repository (full path required)
