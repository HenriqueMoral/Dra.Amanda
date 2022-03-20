function deleteConsulta(pacienteId, procedimentoId, planoId, consultaData) {
    fetch("/delete-consulta", {
      method: "POST",
      body: JSON.stringify({  pacienteId: pacienteId, 
                              procedimentoId:procedimentoId, 
                              planoId: planoId, 
                              consultaData: consultaData }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

function faturarConsulta(pacienteId, procedimentoId, planoId, consultaData) {
    fetch("/faturar-consulta", {
      method: "POST",
      body: JSON.stringify({  pacienteId: pacienteId, 
                              procedimentoId:procedimentoId, 
                              planoId: planoId, 
                              consultaData: consultaData }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
