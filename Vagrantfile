# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos-7.4-x86_64-minimal"
  config.vm.network "forwarded_port", guest: 8080, host: 8080

  config.vm.hostname = "server"
  
  config.vm.provider "virtualbox" do |vb|
    vb = config.vm.hostname
  end
end
