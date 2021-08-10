// $(document).ready(function() {
//     // country state dropdown
//     var $country = $('#country');
//     $state = $('#state');
//     $options = $state.find('option');
//     $("#country").change(function(e) {
//         $state.html($options.filter('[value="'+this.value+'"]'));
//     }).trigger('change');
//
//   });
////////////////////////////////// working above//////////////////////////////////

//car json url country-json
// $.ajax({
//   type:'GET',
//   url: "/Client/country-json",
//   sucess: function(response){
//     console.log(response.data);
//     // const countryData = response.data
//     // countryData.map(item=>{
//     //   const option =  document.createElement('option')
//     //   option.textContent = item.name
//     //   option.setAttribute('value',item.id)
//     // })
//
//   },
//   error: function(error){
//     console.log(error);
//   }
// });
///// get country data end







// //
const subject = document.getElementById('subject')

// select subjects on class change
$('#stud-class').on('change',function(event){
    const class_id = event.target.value;
    subject.innerHTML=""

    $.ajax({
        type:'GET',
        url: "/Teacher/class-subjects/" + class_id,
        success: function(response){
          console.log(response)

          const subjectData = response.data
          //loop through the data
            subjectData.map(item=>{
              const option =  document.createElement('option')
              option.textContent = item.subject
              option.setAttribute('value',item.id)
              subject.appendChild(option)
            });

        },
        error:function(error){
          console.log(error)
        },
      })
});

//
// // populate lga on state change
//
// stateSelect.addEventListener('change', e=>{
//
// const selectedStateId = e.target.value
// lgaSelect.innerHTML=""
//
// $.ajax({
//     type:'GET',
//     url: "/Client/lg-json/" + selectedStateId,
//     success: function(response){
//
//       const lgData = response.data
//       //loop through the data
//         lgData.map(item=>{
//           const option =  document.createElement('option')
//           option.textContent = item.lga
//           option.setAttribute('value',item.id)
//           lgaSelect.appendChild(option)
//         });
//
//     },
//     error:function(error){
//       console.log(error)
//     },
//   })
//
// })

//update ca total on change
const totalca = document.getElementById('totalca')
const exam = document.getElementById('examscore')
const subject_total = document.getElementById('subjecttotal')
const fca = document.getElementById('firstscore')
const sca = document.getElementById('secondscore')
const tca = document.getElementById('thirdscore')
$('#firstscore').on('keyup',function(event){
    const firstscore = event.target.value;
    ca1 = fca.value;
    ca2 = sca.value;
    ca3 = tca.value;
    var total = +ca1 + +ca2 + +ca3;
    // var total = fca.value + sca.value + tca.value

    totalca.value = +total
    subject_total.value = +total + +exam.value
});

$('#secondscore').on('keyup',function(event){
    const secondscore = event.target.value;
    ca1 = fca.value;
    ca2 = sca.value;
    ca3 = tca.value;
    var total = +ca1 + +ca2 + +ca3;
    // var total = fca.value + sca.value + tca.value

    totalca.value = +total
    subject_total.value = +total + +exam.value
});

$('#thirdscore').on('keyup',function(event){
    const thirdscore = event.target.value;

    ca1 = fca.value;
    ca2 = sca.value;
    ca3 = tca.value;
    var total = +ca1 + +ca2 + +ca3;
    // var total = fca.value + sca.value + tca.value

    totalca.value= +total
    subject_total.value = +total + +exam.value
});

// exam score
$('#examscore').on('keyup',function(event){
    const examscore = event.target.value;

    var totalexam = +totalca.value + +examscore;
    // var total = fca.value + sca.value + tca.value

    subject_total.value = +totalexam;
});


//
//
const resultid = document.getElementById('result-id')
$('#comment-table').on('click','#comment-id',function(event){
    resultid.value = $(this).data('id');
    // const session_ = $(this).data('session');
    // const term = $(this).data('term');
    // const classroom = $(this).data('classroom');
    // console.log(resultid)
    // var comm = comment.value = id
    // var totalexam = +totalca.value + +examscore;
    // // var total = fca.value + sca.value + tca.value
    //
    // subject_total.value = +totalexam;
});
