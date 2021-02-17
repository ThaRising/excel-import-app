# -*- mode: ruby -*-
# vi: set ft=ruby :

$kube_setup = <<-'SCRIPT'
cd /application || exit
sudo docker build -t "tharising/django-docker:0.0.1" .

namespace_n=bauerdude
/home/vagrant/bin/helm install django ./service \
    --create-namespace -n "$namespace_n" --set django.service.port="30007"
sudo kubectl config set-context --current --namespace="$namespace_n"
SCRIPT



$tunnel = <<-'SCRIPT'
sudo minikube tunnel &
SCRIPT



Vagrant.configure("2") do |config|
  config.vm.box = "mrvantage/centos7-minikube"
  config.vm.hostname = "vagrantkube"

  for i in 30000..30050
    config.vm.network :forwarded_port, guest: i, host: i
  end

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 2
  end

  config.vm.synced_folder ".", "/application", :mount_options => ['dmode=774', 'fmode=775']
  config.vm.provision :shell, inline: $kube_setup
  config.vm.provision :shell, inline: $tunnel, run: "always", privileged: true
end
